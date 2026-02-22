"""@bruin
name: ingestion.trips
type: python
image: python:3.11

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
  - name: pickup_location_id
    type: integer
  - name: dropoff_location_id
    type: integer
  - name: payment_type
    type: integer
  - name: fare_amount
    type: double
  - name: taxi_type
    type: string
@bruin"""

import json
import os
from typing import Iterable

import pandas as pd


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def _month_starts(start_ts: pd.Timestamp, end_ts: pd.Timestamp) -> Iterable[pd.Timestamp]:
    first_month = pd.Timestamp(year=start_ts.year, month=start_ts.month, day=1)
    last_month = pd.Timestamp(year=end_ts.year, month=end_ts.month, day=1)
    return pd.date_range(first_month, last_month, freq="MS")


def _load_month(taxi_type: str, month_start: pd.Timestamp) -> pd.DataFrame:
    url = f"{BASE_URL}/{taxi_type}_tripdata_{month_start:%Y-%m}.parquet"
    return pd.read_parquet(url)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    column_map = {
      "tpep_pickup_datetime": "pickup_datetime",
      "lpep_pickup_datetime": "pickup_datetime",
      "tpep_dropoff_datetime": "dropoff_datetime",
      "lpep_dropoff_datetime": "dropoff_datetime",
      "PULocationID": "pickup_location_id",
      "DOLocationID": "dropoff_location_id",
    }
    df = df.rename(columns=column_map)

    required = [
      "pickup_datetime",
      "dropoff_datetime",
      "pickup_location_id",
      "dropoff_location_id",
      "payment_type",
      "fare_amount",
    ]
    for col in required:
        if col not in df.columns:
            df[col] = pd.NA

    return df[required].copy()


def _read_taxi_types() -> list[str]:
    raw = os.environ.get("BRUIN_VARS", "{}")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return ["yellow"]

    taxi_types = parsed.get("taxi_types", ["yellow"])
    if not isinstance(taxi_types, list):
        return ["yellow"]
    return [str(x) for x in taxi_types if str(x) in {"yellow", "green"}] or ["yellow"]


def materialize() -> pd.DataFrame:
    start_ts = pd.Timestamp(os.environ["BRUIN_START_DATE"])
    end_ts = pd.Timestamp(os.environ["BRUIN_END_DATE"])
    taxi_types = _read_taxi_types()

    frames: list[pd.DataFrame] = []
    for taxi_type in taxi_types:
        for month_start in _month_starts(start_ts, end_ts):
            monthly = _load_month(taxi_type, month_start)
            monthly = _normalize_columns(monthly)
            monthly["pickup_datetime"] = pd.to_datetime(monthly["pickup_datetime"], errors="coerce")
            monthly["dropoff_datetime"] = pd.to_datetime(monthly["dropoff_datetime"], errors="coerce")
            monthly["taxi_type"] = taxi_type

            # Keep only the interval requested by Bruin.
            monthly = monthly[
                (monthly["pickup_datetime"] >= start_ts)
                & (monthly["pickup_datetime"] < end_ts)
            ]
            frames.append(monthly)

    if not frames:
        return pd.DataFrame(
            columns=[
                "pickup_datetime",
                "dropoff_datetime",
                "pickup_location_id",
                "dropoff_location_id",
                "payment_type",
                "fare_amount",
                "taxi_type",
            ]
        )

    result = pd.concat(frames, ignore_index=True)
    result["pickup_location_id"] = pd.to_numeric(result["pickup_location_id"], errors="coerce").astype("Int64")
    result["dropoff_location_id"] = pd.to_numeric(result["dropoff_location_id"], errors="coerce").astype("Int64")
    result["payment_type"] = pd.to_numeric(result["payment_type"], errors="coerce").astype("Int64")
    result["fare_amount"] = pd.to_numeric(result["fare_amount"], errors="coerce")
    return result

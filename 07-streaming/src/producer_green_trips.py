import argparse
import json
from pathlib import Path
from time import time

import pandas as pd
from kafka import KafkaProducer

REQUIRED_COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount",
]


def _prepare_records(parquet_path: Path) -> list[dict]:
    if not parquet_path.exists():
        raise FileNotFoundError(
            f"Missing parquet file: {parquet_path}. Run setup/download_data.py first."
        )

    df = pd.read_parquet(parquet_path, columns=REQUIRED_COLUMNS)
    for col in ("lpep_pickup_datetime", "lpep_dropoff_datetime"):
        df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d %H:%M:%S")

    return df.to_dict(orient="records")


def produce_green_trips(
    parquet_path: Path, bootstrap_servers: str = "localhost:9092", topic: str = "green-trips"
) -> tuple[int, float]:
    records = _prepare_records(parquet_path)
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )

    t0 = time()
    for record in records:
        producer.send(topic, value=record)

    producer.flush()
    t1 = time()
    producer.close()

    return len(records), t1 - t0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send green taxi trips to Redpanda/Kafka.")
    parser.add_argument(
        "--parquet-path",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "raw" / "green_tripdata_2025-10.parquet",
        help="Path to green trip parquet file.",
    )
    parser.add_argument(
        "--bootstrap-servers", default="localhost:9092", help="Kafka bootstrap servers."
    )
    parser.add_argument("--topic", default="green-trips", help="Topic name.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    count, duration = produce_green_trips(
        parquet_path=args.parquet_path,
        bootstrap_servers=args.bootstrap_servers,
        topic=args.topic,
    )
    print(f"Sent rows: {count}")
    print(f"took {duration:.2f} seconds")


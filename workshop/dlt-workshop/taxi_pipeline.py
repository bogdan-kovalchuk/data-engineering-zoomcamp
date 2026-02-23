"""dlt pipeline for the DE Zoomcamp dlt homework (custom NYC Taxi API)."""

from __future__ import annotations

import argparse
import re
from typing import Any, Dict, Iterable, Iterator, List, Optional

import dlt
import requests


API_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"


def to_snake_case(name: str) -> str:
    """Convert mixed/camel/Pascal names (e.g. Trip_Pickup_DateTime) to snake_case."""
    name = name.replace("-", "_").replace(" ", "_")
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"_+", "_", name)
    return name.lower().strip("_")


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize API record keys to predictable snake_case names for querying."""
    return {to_snake_case(key): value for key, value in record.items()}


def fetch_pages(
    base_url: str,
    *,
    start_page: int = 1,
    max_pages: Optional[int] = None,
    timeout_seconds: int = 30,
) -> Iterator[List[Dict[str, Any]]]:
    """Yield normalized batches from the paginated API until an empty page is returned."""
    page = start_page
    pages_loaded = 0

    while True:
        response = requests.get(base_url, params={"page": page}, timeout=timeout_seconds)
        response.raise_for_status()
        rows = response.json()

        if not isinstance(rows, list):
            raise ValueError(f"Expected list payload, got {type(rows).__name__}")

        if not rows:
            print(f"Stopping on page {page}: empty payload returned.")
            break

        batch = [normalize_record(row) for row in rows]
        pages_loaded += 1
        print(f"Fetched page {page} with {len(batch)} rows")
        yield batch

        page += 1
        if max_pages is not None and pages_loaded >= max_pages:
            print(f"Stopping after max_pages={max_pages}")
            break


@dlt.resource(name="trips", write_disposition="replace")
def nyc_taxi_trips(
    api_url: str = API_URL,
    start_page: int = 1,
    max_pages: Optional[int] = None,
) -> Iterable[List[Dict[str, Any]]]:
    yield from fetch_pages(api_url, start_page=start_page, max_pages=max_pages)


@dlt.source(name="nyc_taxi_api")
def nyc_taxi_source(
    api_url: str = API_URL,
    start_page: int = 1,
    max_pages: Optional[int] = None,
):
    return nyc_taxi_trips(api_url=api_url, start_page=start_page, max_pages=max_pages)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Load NYC taxi trips from custom API into DuckDB via dlt.")
    parser.add_argument("--pipeline-name", default="taxi_pipeline", help="dlt pipeline name")
    parser.add_argument("--dataset-name", default="nyc_taxi_data", help="Destination dataset/schema name")
    parser.add_argument("--start-page", type=int, default=1, help="Starting API page")
    parser.add_argument("--max-pages", type=int, default=None, help="Limit pages for debugging")
    parser.add_argument("--api-url", default=API_URL, help="Override API base URL")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    pipeline = dlt.pipeline(
        pipeline_name=args.pipeline_name,
        destination="duckdb",
        dataset_name=args.dataset_name,
        progress="log",
    )

    load_info = pipeline.run(
        nyc_taxi_source(
            api_url=args.api_url,
            start_page=args.start_page,
            max_pages=args.max_pages,
        )
    )

    print(load_info)
    print(f"Pipeline: {args.pipeline_name}")
    print(f"Dataset:  {args.dataset_name}")


if __name__ == "__main__":
    main()


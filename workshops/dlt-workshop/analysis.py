"""Compute the answers for the dlt workshop homework from the local DuckDB file."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

import duckdb


def detect_table_name(con: duckdb.DuckDBPyConnection, dataset: str) -> str:
    candidates = [
        f"{dataset}.trips",
        f'"{dataset}"."trips"',
    ]
    for table in candidates:
        try:
            con.execute(f"SELECT 1 FROM {table} LIMIT 1")
            return table
        except duckdb.Error:
            continue
    raise RuntimeError(
        f"Could not find table 'trips' in schema '{dataset}'. "
        "Run the pipeline first or pass the correct --dataset-name."
    )


def get_answers(con: duckdb.DuckDBPyConnection, table: str) -> Tuple[str, str, float, float]:
    q1 = con.execute(
        f"""
        SELECT
          CAST(MIN(CAST(trip_pickup_date_time AS TIMESTAMP)) AS DATE) AS start_date,
          CAST(MAX(CAST(trip_pickup_date_time AS TIMESTAMP)) AS DATE) AS end_date
        FROM {table}
        """
    ).fetchone()

    q2 = con.execute(
        f"""
        SELECT
          100.0 * AVG(CASE WHEN lower(payment_type) = 'credit' THEN 1 ELSE 0 END) AS credit_share_pct
        FROM {table}
        """
    ).fetchone()

    q3 = con.execute(
        f"""
        SELECT ROUND(SUM(COALESCE(CAST(tip_amt AS DOUBLE), 0)), 2) AS total_tips
        FROM {table}
        """
    ).fetchone()

    return str(q1[0]), str(q1[1]), float(q2[0]), float(q3[0])


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze local dlt homework DuckDB output.")
    parser.add_argument("--db-path", default="taxi_pipeline.duckdb", help="Path to DuckDB file")
    parser.add_argument("--dataset-name", default="nyc_taxi_data", help="Schema/dataset used by dlt")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    if not db_path.exists():
        raise SystemExit(f"DuckDB file not found: {db_path}. Run taxi_pipeline.py first.")

    con = duckdb.connect(str(db_path))
    try:
        table = detect_table_name(con, args.dataset_name)
        start_date, end_date, credit_share_pct, total_tips = get_answers(con, table)

        print(f"Using table: {table}")
        print(f"Q1 dataset range: {start_date} to {end_date}")
        print(f"Q2 credit card share: {credit_share_pct:.2f}%")
        print(f"Q3 total tips: ${total_tips:,.2f}")
    finally:
        con.close()


if __name__ == "__main__":
    main()


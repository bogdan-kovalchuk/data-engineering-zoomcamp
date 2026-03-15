import argparse
import subprocess
import sys
from pathlib import Path

import psycopg2

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from consumer_trip_distance import count_trips_distance_gt5
from producer_green_trips import produce_green_trips


def run_subprocess(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def recreate_topic(topic: str) -> None:
    delete_cmd = [
        "docker",
        "exec",
        "workshop-redpanda-1",
        "rpk",
        "topic",
        "delete",
        topic,
    ]
    create_cmd = [
        "docker",
        "exec",
        "workshop-redpanda-1",
        "rpk",
        "topic",
        "create",
        topic,
    ]

    try:
        run_subprocess(delete_cmd)
        print(f"Topic deleted: {topic}")
    except subprocess.CalledProcessError:
        print(f"Topic delete skipped (not found or already removed): {topic}")

    run_subprocess(create_cmd)
    print(f"Topic created: {topic}")


def run_q1() -> None:
    output = run_subprocess(["docker", "exec", "workshop-redpanda-1", "rpk", "version"])
    print("Q1 Redpanda version:")
    print(output)


def run_q2(parquet_path: Path, bootstrap_servers: str, topic: str) -> None:
    count, duration = produce_green_trips(
        parquet_path=parquet_path, bootstrap_servers=bootstrap_servers, topic=topic
    )
    print(f"Q2 sent rows: {count}")
    print(f"Q2 took {duration:.2f} seconds")


def run_q3(bootstrap_servers: str, topic: str, timeout_ms: int) -> None:
    count = count_trips_distance_gt5(
        bootstrap_servers=bootstrap_servers, topic=topic, timeout_ms=timeout_ms
    )
    print(f"Q3 trips with trip_distance > 5: {count}")


def init_db() -> None:
    sql_path = ROOT_DIR / "setup" / "init_postgres.sql"
    sql_text = sql_path.read_text(encoding="utf-8")

    with psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="postgres",
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_text)
    print("PostgreSQL tables initialized for Q4-Q6.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DE Zoomcamp Module 7 helper tasks.")
    parser.add_argument("--q1", action="store_true", help="Run Question 1 (Redpanda version).")
    parser.add_argument("--q2", action="store_true", help="Run Question 2 (producer).")
    parser.add_argument("--q3", action="store_true", help="Run Question 3 (consumer).")
    parser.add_argument("--init-db", action="store_true", help="Create PostgreSQL tables for Q4-Q6.")
    parser.add_argument(
        "--recreate-topic",
        action="store_true",
        help="Delete and create topic before producing data.",
    )
    parser.add_argument("--topic", default="green-trips", help="Kafka topic name.")
    parser.add_argument("--bootstrap-servers", default="localhost:9092", help="Kafka bootstrap servers.")
    parser.add_argument(
        "--parquet-path",
        type=Path,
        default=ROOT_DIR / "data" / "raw" / "green_tripdata_2025-10.parquet",
        help="Path to green trip parquet file.",
    )
    parser.add_argument(
        "--timeout-ms",
        default=10000,
        type=int,
        help="Consumer timeout for Q3.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not (args.q1 or args.q2 or args.q3 or args.init_db):
        raise SystemExit("Nothing selected. Use --q1/--q2/--q3/--init-db.")

    if args.recreate_topic:
        recreate_topic(args.topic)

    if args.init_db:
        init_db()
    if args.q1:
        run_q1()
    if args.q2:
        run_q2(args.parquet_path, args.bootstrap_servers, args.topic)
    if args.q3:
        run_q3(args.bootstrap_servers, args.topic, args.timeout_ms)


import argparse
import json

from kafka import KafkaConsumer


def count_trips_distance_gt5(
    bootstrap_servers: str = "localhost:9092",
    topic: str = "green-trips",
    timeout_ms: int = 10000,
) -> int:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=None,
        consumer_timeout_ms=timeout_ms,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    count = 0
    for message in consumer:
        trip_distance = message.value.get("trip_distance")
        if trip_distance is None:
            continue
        if float(trip_distance) > 5.0:
            count += 1

    consumer.close()
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Count trips with trip_distance > 5.")
    parser.add_argument(
        "--bootstrap-servers", default="localhost:9092", help="Kafka bootstrap servers."
    )
    parser.add_argument("--topic", default="green-trips", help="Topic name.")
    parser.add_argument(
        "--timeout-ms",
        default=10000,
        type=int,
        help="Consumer timeout in milliseconds when no new data arrives.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    count = count_trips_distance_gt5(
        bootstrap_servers=args.bootstrap_servers, topic=args.topic, timeout_ms=args.timeout_ms
    )
    print(f"Trips with trip_distance > 5: {count}")


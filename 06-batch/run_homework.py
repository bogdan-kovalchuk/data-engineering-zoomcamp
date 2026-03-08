import argparse
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def build_spark() -> SparkSession:
    return (
        SparkSession.builder.master("local[*]")
        .appName("de-zoomcamp-hw6")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def read_yellow(spark: SparkSession, base_dir: Path):
    yellow_path = base_dir / "data" / "raw" / "yellow_tripdata_2025-11.parquet"
    if not yellow_path.exists():
        raise FileNotFoundError(
            f"Missing file: {yellow_path}. Run setup/download_data.py first."
        )
    return spark.read.parquet(str(yellow_path))


def read_zones(spark: SparkSession, base_dir: Path):
    zones_path = base_dir / "data" / "raw" / "taxi_zone_lookup.csv"
    if not zones_path.exists():
        raise FileNotFoundError(
            f"Missing file: {zones_path}. Run setup/download_data.py first."
        )
    return spark.read.option("header", True).option("inferSchema", True).csv(
        str(zones_path)
    )


def run_q1(spark: SparkSession) -> None:
    print(f"Q1 Spark version: {spark.version}")


def run_q2(yellow_df, base_dir: Path) -> None:
    output_dir = base_dir / "output" / "yellow_2025_11_repartitioned"
    yellow_df.repartition(4).write.mode("overwrite").parquet(str(output_dir))

    parquet_files = list(output_dir.glob("*.parquet"))
    if not parquet_files:
        raise RuntimeError(f"No parquet files found under: {output_dir}")

    avg_mb = sum(p.stat().st_size for p in parquet_files) / len(parquet_files) / (
        1024 * 1024
    )
    print(f"Q2 average parquet file size (MB): {avg_mb:.2f}")
    print(f"Q2 output path: {output_dir}")


def run_q3(yellow_df) -> None:
    trips = (
        yellow_df.filter(F.to_date("tpep_pickup_datetime") == F.lit("2025-11-15"))
        .count()
    )
    print(f"Q3 trips started on 2025-11-15: {trips}")


def run_q4(yellow_df) -> None:
    longest_hours = (
        yellow_df.select(
            ((
                F.unix_timestamp("tpep_dropoff_datetime")
                - F.unix_timestamp("tpep_pickup_datetime")
            )
            / F.lit(3600)).alias("duration_hours")
        )
        .agg(F.max("duration_hours").alias("max_hours"))
        .collect()[0]["max_hours"]
    )
    print(f"Q4 longest trip (hours): {float(longest_hours):.2f}")


def run_q5(spark: SparkSession) -> None:
    ui_url = spark.sparkContext.uiWebUrl
    if ui_url:
        print(f"Q5 Spark UI URL: {ui_url}")
    else:
        print("Q5 Spark UI default port: 4040")


def run_q6(spark: SparkSession, yellow_df, base_dir: Path) -> None:
    zones_df = read_zones(spark, base_dir)

    result = (
        yellow_df.groupBy("PULocationID")
        .count()
        .join(zones_df, yellow_df["PULocationID"] == zones_df["LocationID"], "left")
        .select("Zone", "count")
        .orderBy(F.col("count").asc(), F.col("Zone").asc())
        .limit(1)
        .collect()
    )

    if not result:
        raise RuntimeError("Q6 query returned no rows.")

    print(f"Q6 least frequent pickup zone: {result[0]['Zone']} ({result[0]['count']})")


def parse_args():
    parser = argparse.ArgumentParser(description="Run DE Zoomcamp Module 6 homework tasks.")
    parser.add_argument("--run-all", action="store_true", help="Run all questions.")
    parser.add_argument("--q1", action="store_true", help="Run Question 1.")
    parser.add_argument("--q2", action="store_true", help="Run Question 2.")
    parser.add_argument("--q3", action="store_true", help="Run Question 3.")
    parser.add_argument("--q4", action="store_true", help="Run Question 4.")
    parser.add_argument("--q5", action="store_true", help="Run Question 5.")
    parser.add_argument("--q6", action="store_true", help="Run Question 6.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if not (
        args.run_all or args.q1 or args.q2 or args.q3 or args.q4 or args.q5 or args.q6
    ):
        raise SystemExit(
            "Nothing selected. Use --run-all or at least one of --q1..--q6."
        )

    base_dir = Path(__file__).resolve().parent
    spark = build_spark()

    try:
        run_all = args.run_all
        need_yellow = run_all or args.q2 or args.q3 or args.q4 or args.q6
        yellow_df = read_yellow(spark, base_dir) if need_yellow else None

        if run_all or args.q1:
            run_q1(spark)
        if run_all or args.q2:
            run_q2(yellow_df, base_dir)
        if run_all or args.q3:
            run_q3(yellow_df)
        if run_all or args.q4:
            run_q4(yellow_df)
        if run_all or args.q5:
            run_q5(spark)
        if run_all or args.q6:
            run_q6(spark, yellow_df, base_dir)
    finally:
        spark.stop()

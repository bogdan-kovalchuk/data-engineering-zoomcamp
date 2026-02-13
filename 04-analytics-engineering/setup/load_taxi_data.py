import duckdb
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
YEARS = (2019, 2020)
TAXI_TYPES = ("yellow", "green")
DB_PATH = "taxi_rides_ny.duckdb"


def download_and_convert_files(taxi_type: str) -> None:
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for year in YEARS:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename
            if parquet_filepath.exists():
                print(f"Skipping {parquet_filename} (already exists)")
                continue

            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True, timeout=120)
            response.raise_for_status()
            with open(csv_gz_filepath, "wb") as out:
                for chunk in response.iter_content(chunk_size=8192):
                    out.write(chunk)

            print(f"Converting {csv_gz_filename} to Parquet...")
            con = duckdb.connect()
            con.execute(
                f"""
                COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                TO '{parquet_filepath}' (FORMAT PARQUET)
                """
            )
            con.close()
            csv_gz_filepath.unlink(missing_ok=True)
            print(f"Completed {parquet_filename}")


def update_gitignore() -> None:
    gitignore_path = Path(".gitignore")
    content = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    if "data/" not in content:
        suffix = "\n# Data directory\ndata/\n" if content else "# Data directory\ndata/\n"
        gitignore_path.write_text(content + suffix, encoding="utf-8")


def load_to_duckdb() -> None:
    con = duckdb.connect(DB_PATH)
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in TAXI_TYPES:
        con.execute(
            f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
            """
        )
    con.close()


if __name__ == "__main__":
    update_gitignore()
    for taxi_type in TAXI_TYPES:
        download_and_convert_files(taxi_type)
    load_to_duckdb()
    print("Finished loading yellow and green taxi data into DuckDB.")

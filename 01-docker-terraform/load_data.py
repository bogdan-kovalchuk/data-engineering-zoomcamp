import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5433/ny_taxi"
)

pd.read_parquet("green_tripdata_2025-11.parquet") \
  .to_sql("green_tripdata_2025_11", engine, if_exists="replace", index=False)

pd.read_csv("taxi_zone_lookup.csv") \
  .to_sql("taxi_zone_lookup", engine, if_exists="replace", index=False)
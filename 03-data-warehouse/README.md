# Module 3 Homework: Data Warehousing & BigQuery

This repository contains:
- homework answers: `03-homework.md`
- script to upload parquet files to GCS: `load_yellow_taxi_data.py`
- SQL for BigQuery setup and homework queries: `BigQuery/big_query_hw.sql`

## 1) Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Update these values in `load_yellow_taxi_data.py`:
- `BUCKET_NAME`
- `CREDENTIALS_FILE` (or use `gcloud auth application-default login`)

Example bucket name:
- `dezoomcamp-hw3-bogdan`

## 2) Upload data to GCS

```powershell
python load_yellow_taxi_data.py
```

Expected 6 files in the bucket:
- `yellow_tripdata_2024-01.parquet`
- `yellow_tripdata_2024-02.parquet`
- `yellow_tripdata_2024-03.parquet`
- `yellow_tripdata_2024-04.parquet`
- `yellow_tripdata_2024-05.parquet`
- `yellow_tripdata_2024-06.parquet`

## 3) BigQuery

Run SQL from:
- `BigQuery/big_query_hw.sql`

This file already includes:
- external table creation
- regular table creation
- partitioned and clustered table creation
- queries for all homework questions

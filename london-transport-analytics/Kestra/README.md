# Kestra Ingestion

This module contains the workflow orchestration layer for the raw ingestion stage of **London Transport Analytics**.

The current goal of this stage is straightforward:

1. Download the official TfL dataset as a raw CSV file.
2. Store the raw file in **Google Cloud Storage** as the project data lake.
3. Keep the ingestion logic reproducible and easy to rerun.

## Files

- `docker-compose.yml` -> local Kestra environment
- `set_kv.yaml` -> initializes required project KV variables
- `data_load_gcs.yaml` -> downloads the dataset and uploads it to GCS
- `gcs_to_bigquery_raw.yaml` -> loads the latest raw CSV from GCS into BigQuery
- `build_mart_bigquery.yaml` -> builds the transformed mart table in BigQuery
- `build_dashboard_views_bigquery.yaml` -> builds BigQuery views for the dashboard tiles
- `end_to_end_pipeline.yaml` -> orchestrates the full batch pipeline from source to dashboard-ready layer

## Prerequisites

- Docker Desktop
- A GCP project
- A GCS bucket created for the data lake
- A GCP service account with permission to write to the bucket

## Start Kestra

```bash
cd Kestra
docker-compose up
```

After Kestra starts, open `http://localhost:8080`.

Default local credentials:

- Username: `admin@localhost.dev`
- Password: `kestra`

## Required Secrets and KV Values

Before running the ingestion flow, configure:

- Secret `GCP_SERVICE_ACCOUNT`
- KV `GCP_PROJECT_ID`
- KV `GCP_LOCATION`
- KV `GCP_BUCKET_NAME`
- KV `DATASET_URL`
- KV `BQ_DATASET_NAME`
- KV `BQ_RAW_TABLE_NAME`
- KV `BQ_MART_TABLE_NAME`
- KV `BQ_DASHBOARD_TIME_VIEW_NAME`
- KV `BQ_DASHBOARD_CATEGORY_VIEW_NAME`

You can initialize the KV values by importing and running `set_kv.yaml`.

The `GCP_SERVICE_ACCOUNT` secret should contain the full JSON credentials of your service account.

## Flow Overview

`data_load_gcs.yaml` performs the following steps:

1. Downloads the raw TfL CSV file with Python.
2. Performs a lightweight validation to ensure the file is not empty.
3. Uploads the raw file to GCS under a partition-like landing path.
4. Cleans temporary execution files.

`gcs_to_bigquery_raw.yaml` performs the following steps:

1. Finds the latest raw CSV file in the GCS landing path.
2. Loads the file into a BigQuery raw table.
3. Preserves the source columns as raw strings for downstream transformation.

`build_mart_bigquery.yaml` performs the following steps:

1. Reads the raw BigQuery table.
2. Parses dates and numeric fields.
3. Reshapes transport columns into a long-format analytical mart.
4. Creates a partitioned and clustered BigQuery table for dashboard usage.

`build_dashboard_views_bigquery.yaml` performs the following steps:

1. Reads the transformed mart table.
2. Builds a time-series dashboard view.
3. Builds a transport distribution dashboard view.

`end_to_end_pipeline.yaml` orchestrates the full batch workflow:

1. Source dataset -> GCS raw
2. GCS raw -> BigQuery raw
3. BigQuery raw -> BigQuery mart
4. BigQuery mart -> dashboard views

## Recommended Run Order

1. Import and run `set_kv.yaml`
2. Import the other flow files
3. Run `end_to_end_pipeline.yaml`

## Target GCS Layout

Raw files are uploaded using the following structure:

```text
gs://<bucket>/raw/tfl_journeys_by_type/extract_date=YYYY-MM-DD/tfl_journeys_by_type_YYYY-MM-DD.csv
```

This makes the raw zone easier to query, version, and reprocess later.

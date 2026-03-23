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

You can initialize the KV values by importing and running `set_kv.yaml`.

The `GCP_SERVICE_ACCOUNT` secret should contain the full JSON credentials of your service account.

## Flow Overview

`data_load_gcs.yaml` performs the following steps:

1. Downloads the raw TfL CSV file with Python.
2. Performs a lightweight validation to ensure the file is not empty.
3. Uploads the raw file to GCS under a partition-like landing path.
4. Cleans temporary execution files.

## Target GCS Layout

Raw files are uploaded using the following structure:

```text
gs://<bucket>/raw/tfl_journeys_by_type/extract_date=YYYY-MM-DD/tfl_journeys_by_type_YYYY-MM-DD.csv
```

This makes the raw zone easier to query, version, and reprocess later.

# London Transport Analytics: End-to-End Data Pipeline for Public Transport Insights

## Project Overview

**London Transport Analytics** is a cloud-native data engineering project designed to analyze trends in London's public transport usage through an **end-to-end batch data pipeline**. The project focuses on collecting official transport usage data, storing it in a structured analytics platform, and exposing insights through an interactive dashboard.

The solution is being built to automate the movement of data from the source into a **data lake**, load it into a **data warehouse**, and prepare a clean analytical layer for business-style reporting.

## Problem Statement

Public transport usage changes over time due to seasonality, long-term mobility trends, and external events. Manually collecting and comparing these changes across transport modes is inefficient and makes it harder to identify patterns in demand.

To address this problem, **London Transport Analytics** aims to automate the workflow by:

1. Extracting public transport journey data from an official open dataset.
2. Storing raw data in cloud object storage as a **data lake**.
3. Loading the data from the lake into a **data warehouse**.
4. Transforming the data into a dashboard-ready analytical model.
5. Visualizing trends and category distributions through an interactive dashboard.

The project will focus on journey volumes across major London transport modes, such as:

- Bus
- Underground
- DLR
- Tram
- Overground
- Cable Car

## Current Status

The project is being developed in stages, and the first four stages are already scaffolded.

Completed so far:

- **Stage 1: Data ingestion with Kestra**
- automated download of the official TfL CSV dataset
- upload of raw CSV files into **Google Cloud Storage**
- **Stage 2: Infrastructure with Terraform**
- infrastructure definitions for the **GCS data lake** and **BigQuery dataset**
- **Stage 3: Raw warehouse loading**
- raw load flow from **GCS** into **BigQuery**
- explicit raw schema for the source CSV columns
- latest-file loading strategy from the raw landing zone
- **Stage 4: Transformations**
- dashboard-ready mart table design in **BigQuery**
- parsed dates, typed metrics, and long-format transport modeling
- partitioning by date and clustering by transport type
- dedicated module-level documentation for the implemented stages

Planned next:

- **Stage 5**: publish a dashboard in **Looker Studio**

## Architecture and Highlights

This project follows a batch architecture with the following target flow:

1. **Source dataset** -> official transport dataset file
2. **Data lake** -> raw files stored in cloud object storage
3. **Data warehouse** -> structured tables stored for analytics
4. **Transformations** -> cleaned and modeled tables for reporting
5. **Dashboard** -> visual layer for exploring transport trends

### Solution Highlights

- **Cloud-Native & Infrastructure as Code (IaC)**: the infrastructure layer is defined with **Terraform** for reproducible cloud resource provisioning.
- **Batch Data Pipeline with Workflow Orchestration**: the ingestion and raw loading layers use **Kestra** to orchestrate both `source -> GCS` and `GCS -> BigQuery`.
- **Layered Warehouse Design**: the project already includes both a raw warehouse layer and a transformed mart layer in **BigQuery**.
- **Optimized Data Warehouse**: the transformed mart is designed to be partitioned by date and clustered by transport type.
- **Transformations for Analytics**: the transformation layer parses dates, casts journey values, and reshapes the data into a dashboard-friendly model.
- **Interactive Dashboard**: the final dashboard will present temporal and categorical views of the data.

## Dataset

The project is planned around the **TfL Public Transport Journeys by Type of Transport** dataset.

Planned analytical questions include:

- How has public transport usage changed over time?
- Which transport types contribute the most journeys?
- How do usage patterns differ by month or year?

## Technology Stack

- **Cloud**: GCP
- **Data lake**: Google Cloud Storage
- **Data warehouse**: BigQuery
- **Workflow orchestration**: Kestra
- **Transformations**: BigQuery SQL orchestrated with Kestra
- **Dashboard**: Looker Studio
- **IaC**: Terraform

## Planned Dashboard

The dashboard is expected to include at least two tiles:

- **Temporal distribution**: journey volume over time
- **Categorical distribution**: journey volume by transport type

Additional filters and visuals may be added during implementation.

## Repository Structure

This section reflects the repository structure after implementing the first four project stages:

```text
london-transport-analytics/
|-- README.md
|-- Terraform/
|-- Kestra/
|-- warehouse/
|-- transformations/
|-- dashboard/
|-- images/
```

## Infrastructure Setup

The second implemented stage of the project defines the cloud infrastructure layer with **Terraform**.

Provisioned resources:

- **Google Cloud Storage bucket** for the raw data lake
- **BigQuery dataset** for downstream analytical tables

Terraform files and setup instructions are available in [Terraform/README.md](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Terraform/README.md).

### Implemented Infrastructure Components

- [Terraform/main.tf](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Terraform/main.tf) -> provider and resource definitions
- [Terraform/variables.tf](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Terraform/variables.tf) -> configurable inputs
- [Terraform/outputs.tf](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Terraform/outputs.tf) -> provisioned resource outputs
- [Terraform/terraform.tfvars.example](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Terraform/terraform.tfvars.example) -> example runtime configuration
- [Terraform/setup.ps1](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Terraform/setup.ps1) -> credentials helper
- [Terraform/deploy.ps1](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Terraform/deploy.ps1) -> init/plan/apply helper

## Data Ingestion

The first implemented stage of the project uses **Kestra** to automate raw data ingestion into the data lake.

The ingestion flow will:

- download the official TfL CSV dataset
- validate and store the file as a raw execution artifact
- upload the raw CSV into a GCS bucket
- organize files under a date-based raw landing path

Implementation details and run instructions are available in [Kestra/README.md](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/README.md).

### Implemented Ingestion Components

- [Kestra/docker-compose.yml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/docker-compose.yml) -> local Kestra environment
- [Kestra/set_kv.yaml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/set_kv.yaml) -> project KV initialization
- [Kestra/data_load_gcs.yaml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/data_load_gcs.yaml) -> end-to-end raw ingestion flow
- [Kestra/gcs_to_bigquery_raw.yaml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/gcs_to_bigquery_raw.yaml) -> raw load flow from GCS to BigQuery

### Target Raw Layout

```text
gs://<bucket>/raw/tfl_journeys_by_type/extract_date=YYYY-MM-DD/tfl_journeys_by_type_YYYY-MM-DD.csv
```

## Transformations

The fourth implemented stage builds the first dashboard-ready analytical mart.

The transformation layer is responsible for:

- parsing reporting dates from the raw source
- casting journey metrics into numeric fields
- reshaping transport columns from wide to long format
- producing a mart table optimized for dashboard queries

### Implemented Transformation Components

- [Kestra/build_mart_bigquery.yaml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/build_mart_bigquery.yaml) -> BigQuery mart build flow
- [transformations/README.md](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/transformations/README.md) -> transformation layer documentation

## Data Warehousing

The third implemented stage introduces the initial warehouse loading step.

The current warehouse layer is responsible for:

- locating the latest raw CSV in **GCS**
- loading that file into a **BigQuery raw table**
- preserving source columns in a raw schema for downstream transformations
- keeping the source structure close to the original file before modeling

### Implemented Warehouse Components

- [Kestra/gcs_to_bigquery_raw.yaml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/gcs_to_bigquery_raw.yaml) -> latest-file raw load from GCS to BigQuery
- [warehouse/README.md](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/warehouse/README.md) -> raw warehouse layer documentation

Current warehouse documentation is available in [warehouse/README.md](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/warehouse/README.md).

## Dashboard

This section will describe:

- dashboard design
- chart definitions
- access instructions

This stage has not been implemented yet.

## Reproducibility

At the current stage, the project already includes reproducible files for:

- local workflow orchestration with **Kestra**
- raw ingestion into **GCS**
- infrastructure provisioning with **Terraform**
- raw loading from **GCS** into **BigQuery**
- raw warehouse schema definition inside the loading flow
- transformed mart creation inside **BigQuery**

The full project reproducibility guide will later describe:

- full setup steps
- required credentials and environment variables
- command sequence to reproduce the pipeline

For the current ingestion stage, you will need:

- Docker Desktop
- a GCP project
- a GCS bucket
- a GCP service account JSON secret
- configured Kestra KV values and secrets

For the current infrastructure stage, you will also need:

- Terraform CLI
- a `terraform.tfvars` file based on the provided example
- `GOOGLE_APPLICATION_CREDENTIALS` pointing to your service account JSON

## Future Improvement Opportunities

- Build the final Looker Studio dashboard
- Add automated scheduling for periodic refreshes
- Add data quality checks
- Introduce richer analytical dimensions

## Acknowledgments

This project is being prepared as a course project for data engineering practice, using open public transport data and a cloud-based analytics stack.

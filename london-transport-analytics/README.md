# London Transport Analytics: End-to-End Data Pipeline for Public Transport Insights

## Project Overview

**London Transport Analytics** is a cloud-native data engineering project designed to analyze trends in London's public transport usage through an **end-to-end batch data pipeline**. The project focuses on collecting official transport usage data, storing it in a structured analytics platform, and exposing insights through an interactive dashboard.

The solution is intended to automate the movement of data from the source into a **data lake**, process and model it inside a **data warehouse**, and prepare a clean analytical layer for business-style reporting.

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

## Architecture and Highlights

This project will follow a batch architecture with the following target flow:

1. **Source dataset** -> official transport dataset file
2. **Data lake** -> raw files stored in cloud object storage
3. **Data warehouse** -> structured tables stored for analytics
4. **Transformations** -> cleaned and modeled tables for reporting
5. **Dashboard** -> visual layer for exploring transport trends

### Planned Solution Highlights

- **Cloud-Native & Infrastructure as Code (IaC)**: cloud resources will be provisioned and managed using an IaC tool.
- **Batch Data Pipeline with Workflow Orchestration**: ingestion and loading steps will be automated through an orchestrated workflow.
- **Optimized Data Warehouse**: analytical tables will be partitioned and, where appropriate, clustered for efficient queries.
- **Transformations for Analytics**: transformation logic will prepare reporting-friendly tables for the dashboard.
- **Interactive Dashboard**: the final dashboard will present temporal and categorical views of the data.

## Dataset

The project is planned around the **TfL Public Transport Journeys by Type of Transport** dataset.

Planned analytical questions include:

- How has public transport usage changed over time?
- Which transport types contribute the most journeys?
- How do usage patterns differ by month or year?

## Planned Technology Stack

- **Cloud**: GCP
- **Data lake**: Google Cloud Storage
- **Data warehouse**: BigQuery
- **Workflow orchestration**: Kestra
- **Transformations**: To be finalized
- **Dashboard**: Looker Studio
- **IaC**: Terraform

## Planned Dashboard

The dashboard is expected to include at least two tiles:

- **Temporal distribution**: journey volume over time
- **Categorical distribution**: journey volume by transport type

Additional filters and visuals may be added during implementation.

## Repository Structure

This section will be updated as the project evolves. A tentative structure is shown below:

```text
london-transport-analytics/
|-- README.md
|-- Terraform/
|-- Kestra/
|-- transformations/
|-- warehouse/
|-- dashboard/
|-- images/
```

## Infrastructure Setup

This section will describe:

- prerequisites
- authentication steps
- Terraform deployment steps
- cleanup instructions

## Data Ingestion

The first implemented stage of the project uses **Kestra** to automate raw data ingestion.

The ingestion flow will:

- download the official TfL CSV dataset
- validate and store the file as a raw execution artifact
- upload the raw CSV into a GCS bucket
- organize files under a date-based raw landing path

Implementation details and run instructions are available in [Kestra/README.md](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/README.md).

## Transformations

This section will describe:

- raw-to-staging logic
- analytical model design
- partitioning and clustering strategy
- transformation execution steps

## Data Warehousing

This section will describe:

- dataset and table design
- schema optimization
- loading strategy from lake to warehouse

## Dashboard

This section will describe:

- dashboard design
- chart definitions
- access instructions

## Reproducibility

This section will describe:

- full setup steps
- required credentials and environment variables
- command sequence to reproduce the pipeline

## Future Improvement Opportunities

- Add automated scheduling for periodic refreshes
- Extend the dashboard with additional transport KPIs
- Add data quality checks
- Introduce richer analytical dimensions

## Acknowledgments

This project is being prepared as a course project for data engineering practice, using open public transport data and a cloud-based analytics stack.

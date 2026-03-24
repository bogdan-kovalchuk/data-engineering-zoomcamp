# Transformations Layer

This module documents the first analytical transformation stage for **London Transport Analytics**.

## Current Scope

The transformation stage builds a dashboard-ready mart table from the raw warehouse table.

The current mart performs:

- date parsing from the raw source strings
- numeric casting for journey metrics
- reshaping from a wide transport layout into a long analytical layout
- partitioning and clustering for downstream query efficiency

## Target Mart Table

- dataset: `london_transport_dw`
- table: `transport_journeys_mart`

## Analytical Model

The transformed mart contains one row per:

- reporting period
- transport type

Key output fields include:

- `period_and_financial_year`
- `reporting_period`
- `days_in_period`
- `period_beginning_date`
- `period_ending_date`
- `year`
- `month`
- `year_month`
- `transport_type`
- `journeys_m`

## Optimization Strategy

The current mart table is designed as:

- **partitioned by** `period_beginning_date`
- **clustered by** `transport_type`

This supports the expected dashboard access patterns:

- time-based trend analysis
- category-based comparisons by transport mode

## Orchestration

The mart build is orchestrated through [build_mart_bigquery.yaml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/build_mart_bigquery.yaml).

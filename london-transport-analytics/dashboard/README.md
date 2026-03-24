# Dashboard Layer

This module defines the dashboard-ready layer for **London Transport Analytics**.

## Current Scope

The current dashboard stage prepares two BigQuery views that can be connected directly to **Looker Studio**.

These two views support the required course visuals:

- one temporal chart
- one categorical chart

## Dashboard Sources

### 1. Time-Series View

- view: `transport_journeys_over_time_v`
- purpose: trend of total transport journeys over time
- recommended chart: line chart
- dimension: `period_beginning_date`
- metric: `total_journeys_m`

### 2. Category Distribution View

- view: `transport_type_distribution_v`
- purpose: total journey volume by transport type
- recommended chart: bar chart
- dimension: `transport_type`
- metric: `total_journeys_m`

## BigQuery View Build

The views are built through [build_dashboard_views_bigquery.yaml](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/Kestra/build_dashboard_views_bigquery.yaml).

For a manual SQL alternative, see [create_dashboard_views.sql](C:/Users/bogdan/Documents/Programming/MLDL/data-engineering-zoomcamp/london-transport-analytics/dashboard/create_dashboard_views.sql).

## Looker Studio Setup

1. Open Looker Studio.
2. Add a BigQuery data source.
3. Connect to the dataset `london_transport_dw`.
4. Build one chart from `transport_journeys_over_time_v`.
5. Build one chart from `transport_type_distribution_v`.
6. Add titles and axis labels to make the dashboard self-explanatory.

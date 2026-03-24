# Warehouse Layer

This module documents the current warehouse stage for **London Transport Analytics**.

## Current Scope

The first warehouse step loads the latest raw CSV file from **GCS** into a **BigQuery raw table**.

This stage intentionally preserves the source structure with minimal interpretation:

- original source columns are retained
- columns are initially loaded as raw strings
- parsing, cleaning, and type conversion are deferred to the transformation layer

## Raw Table

Planned BigQuery raw table:

- dataset: `london_transport_dw`
- table: `transport_journeys_raw`

## Raw Schema

The current raw table keeps the following source fields:

- `period_and_financial_year`
- `reporting_period`
- `days_in_period`
- `period_beginning`
- `period_ending`
- `bus_journeys_m`
- `underground_journeys_m`
- `dlr_journeys_m`
- `tram_journeys_m`
- `overground_journeys_m`
- `london_cable_car_journeys_m`
- `tfl_rail_journeys_m`

## Loading Strategy

The load is orchestrated with `Kestra` through `gcs_to_bigquery_raw.yaml`.

The workflow:

1. Finds the latest raw CSV file in the GCS landing area.
2. Loads the file into BigQuery using an explicit raw schema.
3. Replaces the current raw table snapshot with the most recent load.

## Next Step

The next stage will build transformed analytical tables from this raw layer by:

- parsing dates
- casting numeric fields
- reshaping wide transport columns into a reporting-friendly model

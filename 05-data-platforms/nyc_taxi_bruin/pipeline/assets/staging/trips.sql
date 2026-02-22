/* @bruin
name: staging.trips
type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: pickup_datetime
    type: timestamp
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
  - name: pickup_location_id
    type: integer
  - name: dropoff_location_id
    type: integer
  - name: payment_type
    type: string
  - name: fare_amount
    type: double
  - name: taxi_type
    type: string

custom_checks:
  - name: row_count_greater_than_zero
    query: |
      SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END
      FROM staging.trips
      WHERE pickup_datetime >= '{{ start_datetime }}'
        AND pickup_datetime < '{{ end_datetime }}'
    value: 1
@bruin */

WITH base AS (
    SELECT
        t.pickup_datetime,
        t.dropoff_datetime,
        CAST(t.pickup_location_id AS INTEGER) AS pickup_location_id,
        CAST(t.dropoff_location_id AS INTEGER) AS dropoff_location_id,
        COALESCE(p.payment_type_name, 'unknown') AS payment_type,
        CAST(t.fare_amount AS DOUBLE) AS fare_amount,
        t.taxi_type,
        ROW_NUMBER() OVER (
            PARTITION BY
                t.pickup_datetime,
                t.dropoff_datetime,
                t.pickup_location_id,
                t.dropoff_location_id,
                t.fare_amount,
                t.taxi_type
            ORDER BY t.pickup_datetime
        ) AS rn
    FROM ingestion.trips AS t
    LEFT JOIN ingestion.payment_lookup AS p
        ON t.payment_type = p.payment_type_id
    WHERE t.pickup_datetime >= '{{ start_datetime }}'
      AND t.pickup_datetime < '{{ end_datetime }}'
      AND t.pickup_datetime IS NOT NULL
)
SELECT
    pickup_datetime,
    dropoff_datetime,
    pickup_location_id,
    dropoff_location_id,
    payment_type,
    fare_amount,
    taxi_type
FROM base
WHERE rn = 1

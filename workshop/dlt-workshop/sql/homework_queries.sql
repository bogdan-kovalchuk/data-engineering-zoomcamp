-- Run after `python taxi_pipeline.py`
-- Assumes pipeline_name=taxi_pipeline and dataset_name=nyc_taxi_data

-- Q1: Start/end date of the dataset
SELECT
  CAST(MIN(CAST(trip_pickup_date_time AS TIMESTAMP)) AS DATE) AS start_date,
  CAST(MAX(CAST(trip_pickup_date_time AS TIMESTAMP)) AS DATE) AS end_date
FROM nyc_taxi_data.trips;

-- Q2: Proportion of trips paid with credit card
SELECT
  ROUND(100.0 * AVG(CASE WHEN lower(payment_type) = 'credit' THEN 1 ELSE 0 END), 2) AS credit_share_pct
FROM nyc_taxi_data.trips;

-- Q3: Total tips amount
SELECT
  ROUND(SUM(COALESCE(CAST(tip_amt AS DOUBLE), 0)), 2) AS total_tips
FROM nyc_taxi_data.trips;


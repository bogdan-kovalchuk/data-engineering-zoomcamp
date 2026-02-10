-- Set your project and dataset IDs before running.
-- Example:
--   project_id = dezoomcamp-project
--   dataset_id = dezoomcamp_hw3
--
-- Replace placeholders:
--   <PROJECT_ID>.<DATASET_ID>
--   <GCS_BUCKET_NAME>

-- 1) External table (Parquet from GCS)
CREATE OR REPLACE EXTERNAL TABLE `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024_ext`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://<GCS_BUCKET_NAME>/yellow_tripdata_2024-01.parquet',
    'gs://<GCS_BUCKET_NAME>/yellow_tripdata_2024-02.parquet',
    'gs://<GCS_BUCKET_NAME>/yellow_tripdata_2024-03.parquet',
    'gs://<GCS_BUCKET_NAME>/yellow_tripdata_2024-04.parquet',
    'gs://<GCS_BUCKET_NAME>/yellow_tripdata_2024-05.parquet',
    'gs://<GCS_BUCKET_NAME>/yellow_tripdata_2024-06.parquet'
  ]
);

-- 2) Materialized/regular table (non-partitioned, non-clustered)
CREATE OR REPLACE TABLE `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024` AS
SELECT *
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024_ext`;

-- Q1
SELECT COUNT(*) AS total_records
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`;

-- Q2 (run separately and check "estimated bytes processed")
SELECT COUNT(DISTINCT PULocationID) AS distinct_pu
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024_ext`;

SELECT COUNT(DISTINCT PULocationID) AS distinct_pu
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`;

-- Q3 (run separately and compare estimate)
SELECT PULocationID
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`;

SELECT PULocationID, DOLocationID
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`;

-- Q4
SELECT COUNT(*) AS zero_fare_trips
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`
WHERE fare_amount = 0;

-- Q5
CREATE OR REPLACE TABLE `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024_part_clust`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`;

-- Q6: non-partitioned table (note estimated bytes)
SELECT DISTINCT VendorID
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Q6: partitioned+clustered table (note estimated bytes)
SELECT DISTINCT VendorID
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024_part_clust`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Q9
SELECT COUNT(*)
FROM `<PROJECT_ID>.<DATASET_ID>.yellow_taxi_2024`;

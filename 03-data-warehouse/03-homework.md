# Module 3 Homework: Data Warehousing & BigQuery

## Question 1. Counting records

What is count of records for the 2024 Yellow Taxi Data?
- 65,623
- 840,402
- 20,332,093 ✅
- 85,431,289

```sql
SELECT COUNT(*) AS total_records
FROM `dezoomcamp_hw3.yellow_taxi_2024`;
```

## Question 2. Data read estimation

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table ✅
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

```sql
SELECT COUNT(DISTINCT PULocationID) AS distinct_pu
FROM `dezoomcamp_hw3.yellow_taxi_2024_ext`;

SELECT COUNT(DISTINCT PULocationID) AS distinct_pu
FROM `dezoomcamp_hw3.yellow_taxi_2024`;
```

## Question 3. Understanding columnar storage

Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed. ✅
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

```sql
SELECT PULocationID
FROM `dezoomcamp_hw3.yellow_taxi_2024`;

SELECT PULocationID, DOLocationID
FROM `dezoomcamp_hw3.yellow_taxi_2024`;
```

## Question 4. Counting zero fare trips

How many records have a fare_amount of 0?
- 128,210
- 546,578
- 20,188,016
- 8,333 ✅

```sql
SELECT COUNT(*) AS zero_fare_trips
FROM `dezoomcamp_hw3.yellow_taxi_2024`
WHERE fare_amount = 0;
```

## Question 5. Partitioning and clustering

What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?
- Partition by tpep_dropoff_datetime and Cluster on VendorID ✅
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

```sql
CREATE OR REPLACE TABLE `dezoomcamp_hw3.yellow_taxi_2024_part_clust`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `dezoomcamp_hw3.yellow_taxi_2024`;
```

## Question 6. Partition benefits

Choose the answer which most closely matches.
- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table ✅
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

```sql
SELECT DISTINCT VendorID
FROM `dezoomcamp_hw3.yellow_taxi_2024`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM `dezoomcamp_hw3.yellow_taxi_2024_part_clust`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```

## Question 7. External table storage

Where is the data stored in the External Table you created?
- Big Query
- Container Registry
- GCP Bucket ✅
- Big Table

## Question 8. Clustering best practices

It is best practice in Big Query to always cluster your data:
- True
- False ✅

## Question 9. Understanding table scans

```sql
SELECT COUNT(*)
FROM `dezoomcamp_hw3.yellow_taxi_2024`;
```

Estimated bytes: **0 B** (or near-zero metadata read).  
Reason: BigQuery can answer `COUNT(*)` from table metadata, so it does not need to scan all data blocks.

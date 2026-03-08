# Module 6 Homework: Batch Processing with Spark

This homework uses Spark locally to process `yellow_tripdata_2025-11.parquet` and answer all module questions.

---

### Question 1. Install Spark and PySpark

What's the output of `spark.version` in a local Spark session?

- `3.5.5` ✅

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("hw6").getOrCreate()
print(spark.version)  # 3.5.5
```

---

### Question 2. Yellow November 2025

Average parquet file size after repartitioning to 4 partitions and writing to parquet:

- 6MB
- 25MB ✅
- 75MB
- 100MB

```python
from pathlib import Path
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("hw6-q2").getOrCreate()
df = spark.read.parquet("data/raw/yellow_tripdata_2025-11.parquet")

output = "output/yellow_2025_11_repartitioned"
df.repartition(4).write.mode("overwrite").parquet(output)

files = list(Path(output).glob("*.parquet"))
avg_mb = sum(f.stat().st_size for f in files) / len(files) / (1024 * 1024)
print(round(avg_mb, 2))  # ~25 MB
```

---

### Question 3. Count records

How many trips started on `2025-11-15`?

- 62,610 ✅
- 102,340
- 162,604
- 225,768

```sql
SELECT COUNT(*) AS trips_on_2025_11_15
FROM yellow_2025_11
WHERE DATE(tpep_pickup_datetime) = '2025-11-15';
```

---

### Question 4. Longest trip

Maximum trip duration in hours:

- 22.7
- 58.2
- 90.6
- 134.5 ✅

```sql
SELECT
  MAX((UNIX_TIMESTAMP(tpep_dropoff_datetime) - UNIX_TIMESTAMP(tpep_pickup_datetime)) / 3600.0) AS longest_trip_hours
FROM yellow_2025_11;
```

---

### Question 5. User Interface

Default local Spark UI port:

- 80
- 443
- 4040 ✅
- 8080

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("hw6-q5").getOrCreate()
print(spark.sparkContext.uiWebUrl)  # http://localhost:4040
```

---

### Question 6. Least frequent pickup location zone

Least frequent pickup zone:

- Governor's Island/Ellis Island/Liberty Island ✅
- Arden Heights
- Rikers Island
- Jamaica Bay

```sql
SELECT
  z.Zone,
  COUNT(*) AS trips
FROM yellow_2025_11 y
LEFT JOIN taxi_zone_lookup z
  ON y.PULocationID = z.LocationID
GROUP BY z.Zone
ORDER BY trips ASC, z.Zone ASC
LIMIT 1;
```

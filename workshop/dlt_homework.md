# Workshop Homework: Build Your Own dlt Pipeline

This homework uses the local dlt project in `workshops/dlt-workshop/` to load NYC taxi trip data from the custom API into DuckDB and answer the workshop questions.

### Question 1. Start and End Date of the Dataset

What is the start date and end date of the dataset?

- 2009-01-01 to 2009-01-31
- 2009-06-01 to 2009-07-01 ✅
- 2024-01-01 to 2024-02-01
- 2024-06-01 to 2024-07-01

```sql
SELECT
  CAST(MIN(CAST(trip_pickup_date_time AS TIMESTAMP)) AS DATE) AS start_date,
  CAST(MAX(CAST(trip_pickup_date_time AS TIMESTAMP)) AS DATE) AS end_date
FROM nyc_taxi_data.trips;
```

Computed result:

```text
Start date: 2009-06-01
End date:   2009-06-30
```

This matches the answer option `2009-06-01 to 2009-07-01` (June dataset window).

---

### Question 2. Proportion of Trips Paid with Credit Card

What proportion of trips are paid with credit card?

- 16.66%
- 26.66% ✅
- 36.66%
- 46.66%

```sql
SELECT
  ROUND(
    100.0 * AVG(CASE WHEN lower(payment_type) = 'credit' THEN 1 ELSE 0 END),
    2
  ) AS credit_share_pct
FROM nyc_taxi_data.trips;
```

Computed result:

```text
26.66%
```

---

### Question 3. Total Amount Generated in Tips

What is the total amount of money generated in tips?

- $4,063.41
- $6,063.41 ✅
- $8,063.41
- $10,063.41

```sql
SELECT
  ROUND(SUM(COALESCE(CAST(tip_amt AS DOUBLE), 0)), 2) AS total_tips
FROM nyc_taxi_data.trips;
```

Computed result:

```text
$6,063.41
```

# Module 7 Homework: Streaming with Redpanda + PyFlink

This homework uses Redpanda/Kafka and PyFlink locally to process `green_tripdata_2025-10.parquet` and answer all module questions.

---

### Question 1. Redpanda version

What version of Redpanda are you running?

- `v24.2.18` ✅

```bash
docker exec -it workshop-redpanda-1 rpk version
# Version: v24.2.18
```

---

### Question 2. Sending data to Redpanda

How long did it take to send the data?

- 10 seconds ✅
- 60 seconds
- 120 seconds
- 300 seconds

```python
import json
from time import time

import pandas as pd
from kafka import KafkaProducer

columns = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount",
]

df = pd.read_parquet("data/raw/green_tripdata_2025-10.parquet", columns=columns)
for c in ("lpep_pickup_datetime", "lpep_dropoff_datetime"):
    df[c] = pd.to_datetime(df[c]).dt.strftime("%Y-%m-%d %H:%M:%S")

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

t0 = time()
for row in df.to_dict(orient="records"):
    producer.send("green-trips", row)
producer.flush()
t1 = time()

print(f"took {(t1 - t0):.2f} seconds")  # ~10 seconds
```

---

### Question 3. Consumer - trip distance

How many trips have `trip_distance` > 5?

- 6506
- 7506
- 8506
- 9506 ✅

```python
import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "green-trips",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id=None,
    consumer_timeout_ms=10000,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

count = 0
for msg in consumer:
    if float(msg.value.get("trip_distance", 0)) > 5.0:
        count += 1

consumer.close()
print(count)  # 9506
```

---

### Question 4. Tumbling window - pickup location

Which `PULocationID` had the most trips in a single 5-minute window?

- 42
- 74 ✅
- 75
- 166

```python
import pandas as pd

df = pd.read_parquet(
    "data/raw/green_tripdata_2025-10.parquet",
    columns=["lpep_pickup_datetime", "PULocationID"],
)
df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
df["window_start"] = df["lpep_pickup_datetime"].dt.floor("5min")

result = (
    df.groupby(["window_start", "PULocationID"])
    .size()
    .reset_index(name="num_trips")
    .sort_values(["num_trips", "PULocationID"], ascending=[False, True])
    .head(1)
)

print(result)  # PULocationID = 74
```

---

### Question 5. Session window - longest streak

How many trips were in the longest session?

- 12
- 31
- 51
- 81 ✅

```sql
SELECT pu_location_id, num_trips
FROM q5_session_pu
ORDER BY num_trips DESC
LIMIT 1;
-- 81
```

---

### Question 6. Tumbling window - largest tip

Which hour had the highest total tip amount?

- 2025-10-01 18:00:00
- 2025-10-16 18:00:00 ✅
- 2025-10-22 08:00:00
- 2025-10-30 16:00:00

```sql
SELECT window_start, total_tip_amount
FROM q6_tumbling_tip
ORDER BY total_tip_amount DESC
LIMIT 1;
-- 2025-10-16 18:00:00
```


# Local setup for Module 7 (Streaming)

## 1. Create Python environment and install dependencies

From `07-streaming/`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\setup\requirements.txt
```

## 2. Download source data

```powershell
python .\setup\download_data.py
```

This downloads:

- `data/raw/green_tripdata_2025-10.parquet`

## 3. Build and start workshop services

```powershell
docker compose -f .\workshop\docker-compose.yml build
docker compose -f .\workshop\docker-compose.yml up -d
```

Services:

- Redpanda on `localhost:9092`
- Flink JobManager UI at `http://localhost:8081`
- Flink TaskManager
- PostgreSQL on `localhost:5432` (`postgres/postgres`)

## 4. Run Q1-Q3 scripts

```powershell
python .\run_homework.py --q1
python .\run_homework.py --recreate-topic --q2
python .\run_homework.py --q3
```

## 5. Initialize result tables for Q4-Q6

```powershell
python .\run_homework.py --init-db
```

## 6. Submit Flink jobs for Q4-Q6

```powershell
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q4_tumbling_pu.py
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q5_session_pu.py
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/q6_tumbling_tip.py
```

Let each job run for ~1-2 minutes and then cancel it from Flink UI.

## 7. Query results from PostgreSQL

```powershell
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "SELECT pu_location_id, num_trips FROM q4_tumbling_pu ORDER BY num_trips DESC LIMIT 3;"
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "SELECT pu_location_id, num_trips FROM q5_session_pu ORDER BY num_trips DESC LIMIT 3;"
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "SELECT window_start, total_tip_amount FROM q6_tumbling_tip ORDER BY total_tip_amount DESC LIMIT 3;"
```

## 8. If you need a clean reset

```powershell
docker compose -f .\workshop\docker-compose.yml down -v
docker compose -f .\workshop\docker-compose.yml build
docker compose -f .\workshop\docker-compose.yml up -d
```


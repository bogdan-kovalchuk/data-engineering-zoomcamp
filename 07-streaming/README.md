# Module 7 Homework: Streaming with Redpanda + PyFlink

This folder contains a ready-to-run local setup for Homework 7.

## Structure

- `07-homework.md` - homework questions
- `setup/requirements.txt` - Python dependencies for local scripts
- `setup/local_setup.md` - step-by-step setup instructions
- `setup/download_data.py` - downloads source parquet file
- `setup/init_postgres.sql` - result tables for Q4-Q6
- `workshop/` - Docker environment (Redpanda, Flink, PostgreSQL)
- `src/producer_green_trips.py` - Q2 producer
- `src/consumer_trip_distance.py` - Q3 consumer
- `workshop/src/job/q4_tumbling_pu.py` - Q4 Flink job
- `workshop/src/job/q5_session_pu.py` - Q5 Flink job
- `workshop/src/job/q6_tumbling_tip.py` - Q6 Flink job
- `run_homework.py` - helper CLI for Q1-Q3 and setup commands

## Quick Start (PowerShell)

```powershell
cd 07-streaming
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\setup\requirements.txt

python .\setup\download_data.py
docker compose -f .\workshop\docker-compose.yml build
docker compose -f .\workshop\docker-compose.yml up -d

python .\run_homework.py --q1
python .\run_homework.py --recreate-topic --q2 --q3
```

For Q4-Q6, follow `setup/local_setup.md` to submit Flink jobs and query PostgreSQL.


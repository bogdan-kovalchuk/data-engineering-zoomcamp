# Local setup for Module 6 (Spark)

## 1. Create Python environment and install dependencies

From `06-batch/`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\setup\requirements.txt
```

## 2. Download source files

```powershell
python .\setup\download_data.py
```

This downloads:

- `data/raw/yellow_tripdata_2025-11.parquet`
- `data/raw/taxi_zone_lookup.csv`

## 3. Run homework workload

```powershell
python .\run_homework.py --run-all
```

## 4. Notes for homework questions

- Q1: Spark version is printed by `--q1` or `--run-all`.
- Q2: Repartitioned parquet files are written to `output/yellow_2025_11_repartitioned/`.
- Q3: The script counts trips with pickup date `2025-11-15`.
- Q4: The script computes max trip duration in hours.
- Q5: Default Spark UI is on port `4040` (also printed in script output).
- Q6: The script joins with `taxi_zone_lookup.csv` and finds the least frequent pickup zone.

## 5. Optional separate runs

```powershell
python .\run_homework.py --q1 --q5
python .\run_homework.py --q2
python .\run_homework.py --q3 --q4 --q6
```

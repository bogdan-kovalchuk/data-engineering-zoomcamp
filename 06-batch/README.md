# Module 6 Homework: Batch Processing with Spark

This folder now contains a ready-to-run local setup for Homework 6.

## Structure

- `homework.md` - homework questions
- `setup/requirements.txt` - Python dependencies
- `setup/local_setup.md` - step-by-step setup instructions
- `setup/download_data.py` - downloads required source files
- `run_homework.py` - runs all required Spark computations
- `.gitignore` - ignores local datasets and Spark outputs

## Quick Start (PowerShell)

```powershell
cd 06-batch
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\setup\requirements.txt
python .\setup\download_data.py
python .\run_homework.py --run-all
```

## Useful Commands

```powershell
# only repartition/write parquet files for Q2
python .\run_homework.py --q2

# only analytical questions (Q3, Q4, Q6)
python .\run_homework.py --q3 --q4 --q6

# print Spark version and UI info (Q1, Q5)
python .\run_homework.py --q1 --q5
```

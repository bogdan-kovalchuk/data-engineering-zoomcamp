# dlt Workshop Homework Environment (NYC Taxi API)

Ready-to-run local environment for the dlt workshop homework (custom API -> DuckDB), organized in the same style as modules `04/05`:

- `setup/` - setup instructions and dependencies
- `taxi_pipeline.py` - ready dlt pipeline for the API with pagination
- `analysis.py` - local helper script to compute homework answers
- `sql/homework_queries.sql` - SQL queries for manual verification
- `dlt-workshop-homework.md` - notes/answers template for the homework

## Quick Start (Windows PowerShell)

```powershell
cd workshops\dlt-workshop
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\setup\requirements.txt
python .\taxi_pipeline.py
python .\analysis.py
```

Detailed steps: `setup/local_setup.md`.

# dlt Workshop Homework Environment (NYC Taxi API)

Ready-to-run local environment for the dlt workshop homework (custom API -> DuckDB), organized in the same style as modules `04/05`:

- `setup/` - setup instructions and dependencies
- `taxi_pipeline.py` - ready dlt pipeline for the API with pagination
- `analysis.py` - local helper script to compute homework answers
- `sql/homework_queries.sql` - SQL queries for manual verification
- `dlt-workshop-homework.md` - notes/answers template for the homework

## What This Project Does

This local project loads NYC Yellow Taxi trip data from the custom workshop API into DuckDB using `dlt`, then provides helper scripts/queries to answer the homework questions.

API details used by the pipeline:

- Base URL: `https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api`
- Response format: paginated JSON array
- Page size: `1000` rows
- Pagination strategy: request `page=1,2,3,...` and stop when an empty page is returned

## Project Structure

- `taxi_pipeline.py` - dlt pipeline (custom API -> DuckDB)
- `analysis.py` - computes homework answers from the DuckDB output
- `sql/homework_queries.sql` - SQL equivalents for manual checks
- `setup/requirements.txt` - Python dependencies
- `setup/local_setup.md` - detailed setup notes (secondary reference)
- `setup/mcp/` - dlt MCP config examples for Cursor / VS Code
- `dlt-workshop-homework.md` - local notes template

## Setup (Windows PowerShell)

### 1. Open the project folder

```powershell
cd C:\Users\bogdan\Documents\Programming\MLDL\data-engineering-zoomcamp\workshops\dlt-workshop
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Then activate the environment again.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r .\setup\requirements.txt
```

This installs the packages needed for:

- `dlt` + DuckDB destination
- local analysis with `duckdb`
- optional notebook/report tooling (`marimo`, `ibis`, `altair`)

### 4. (Optional) Configure dlt MCP server in your IDE

This is optional for running the code, but useful if you want AI assistance to inspect pipeline metadata.

Cursor:

- Use `setup/mcp/cursor-mcp.json` as the MCP server config template

VS Code (Copilot):

- Use `setup/mcp/vscode-mcp.json` as the `.vscode/mcp.json` template

These configs run:

```bash
uv run --with "dlt[duckdb]" --with "dlt-mcp[search]" python -m dlt_mcp
```

## Run the Pipeline

### 1. Execute the dlt pipeline

```powershell
python .\taxi_pipeline.py
```

What happens during execution:

- the script calls the workshop custom API
- fetches pages in sequence (`page=1,2,3,...`)
- normalizes JSON keys to `snake_case`
- loads records into DuckDB via `dlt`
- stops when the API returns an empty page

Default runtime settings:

- `pipeline_name = taxi_pipeline`
- `dataset_name = nyc_taxi_data`
- output DB file: `taxi_pipeline.duckdb`
- destination table: `nyc_taxi_data.trips`

### 2. Debug run (optional)

Use a smaller page count when testing:

```powershell
python .\taxi_pipeline.py --max-pages 3
```

## Inspect and Answer the Homework

### Option A: Use the helper analysis script (recommended)

```powershell
python .\analysis.py
```

This prints:

- dataset start/end date
- share of `Credit` payments
- total tips amount

### Option B: Run SQL manually

Use the queries in:

- `sql/homework_queries.sql`

You can query the DuckDB file with DuckDB CLI or any SQL client that supports DuckDB.

## dlt Dashboard (Optional, part of the workshop flow)

```powershell
dlt pipeline taxi_pipeline show
```

This lets you inspect:

- pipeline runs
- schemas and tables
- loaded data and metadata

## Quick Start (Short Version)

```powershell
cd C:\Users\bogdan\Documents\Programming\MLDL\data-engineering-zoomcamp\workshops\dlt-workshop
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\setup\requirements.txt
python .\taxi_pipeline.py
python .\analysis.py
```

## Notes

- The file `workshops/dlt_homework.md` contains the final homework answers in a compact format.
- `setup/local_setup.md` contains the same setup flow in a separate guide if you prefer a split setup/reference structure.

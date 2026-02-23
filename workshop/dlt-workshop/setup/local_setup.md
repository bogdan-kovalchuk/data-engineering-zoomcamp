# Local setup for dlt workshop homework (custom NYC Taxi API)

## 1. What is already prepared in this repo

This folder already includes the files you need to complete the homework without running `dlt init`:

- `taxi_pipeline.py` - dlt pipeline for the custom API with pagination (`page=1..N`, stop on empty page)
- `analysis.py` - helper script to compute the answers to the 3 homework questions
- `sql/homework_queries.sql` - the same checks in SQL format
- `setup/mcp/` - example dlt MCP server configs for Cursor / VS Code

## 2. Create and activate virtual environment

Windows PowerShell:

```powershell
cd workshops\dlt-workshop
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\setup\requirements.txt
```

Optional (`uv` instead of `pip`):

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r .\setup\requirements.txt
```

## 3. (Optional) Configure dlt MCP server in your IDE

Use one of these examples:

- Cursor: `setup/mcp/cursor-mcp.json`
- VS Code (Copilot): `setup/mcp/vscode-mcp.json`

MCP is not required to run the pipeline, but it is useful for exploring pipeline metadata.

## 4. Run the pipeline

```powershell
python .\taxi_pipeline.py
```

What the script does:

- loads NYC Yellow Taxi trips from the custom API
- iterates through pages (`page=1,2,3,...`)
- stops when the API returns an empty list
- stores the data in DuckDB via dlt

Defaults:

- `pipeline_name = taxi_pipeline`
- `dataset_name = nyc_taxi_data`
- local DB file: `taxi_pipeline.duckdb` (standard for dlt/DuckDB)

## 5. Inspect pipeline (optional, but part of workshop)

```powershell
dlt pipeline taxi_pipeline show
```

## 6. Answer homework questions

### Option A: Python helper script (fastest)

```powershell
python .\analysis.py
```

The script prints:

- start/end date dataset
- share of `Credit` payments
- total tips amount

### Option B: SQL manually in DuckDB

Open DuckDB CLI (or any DuckDB client) and run the queries from:

- `sql/homework_queries.sql`

## 7. Useful rerun modes

Full rerun (the script already uses `write_disposition="replace"`):

```powershell
python .\taxi_pipeline.py
```

Quick test run with only a few pages (for debugging):

```powershell
python .\taxi_pipeline.py --max-pages 3
```

## 8. Notes / troubleshooting

- If PowerShell blocks venv activation: `Set-ExecutionPolicy -Scope Process Bypass`
- If the `dlt` command is not found, run it from the activated venv or use `python -m dlt`
- If you want to inspect tables manually:

```powershell
python -c "import duckdb; con=duckdb.connect('taxi_pipeline.duckdb'); print(con.execute('show tables').fetchall())"
```

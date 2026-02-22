# Local setup for Module 5 (Bruin)

## 1. Install Bruin CLI

Windows (PowerShell):

```powershell
winget install Bruin.Bruin
```

Alternative (Git Bash / WSL / macOS / Linux):

```bash
curl -LsSf https://getbruin.com/install/cli | sh
```

Check installation:

```powershell
bruin --version
```

## 2. Project structure in this repository

This module already contains a ready-to-run Bruin project:

- `nyc_taxi_bruin/` - Bruin project root
- `nyc_taxi_bruin/.bruin.yml` - project connections
- `nyc_taxi_bruin/pipeline/pipeline.yml` - pipeline config
- `nyc_taxi_bruin/pipeline/assets/` - ingestion, staging, reports assets

## 3. Run the pipeline

```powershell
cd ..\nyc_taxi_bruin
bruin validate .\pipeline\pipeline.yml
bruin run .\pipeline\pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01
```

## 4. Useful commands for homework

```powershell
bruin lineage .\pipeline\pipeline.yml
bruin run --select ingestion.trips+ .\pipeline\pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01
bruin run .\pipeline\pipeline.yml --full-refresh
```

## 5. Notes

- The DuckDB file is stored locally as `nyc_taxi_bruin\duckdb.db`.
- Python dependencies for the ingestion asset are in `pipeline/assets/ingestion/requirements.txt`.
- Default `taxi_types` is `["yellow"]`; override with:

```powershell
bruin run .\pipeline\pipeline.yml --var 'taxi_types=["yellow"]'
```

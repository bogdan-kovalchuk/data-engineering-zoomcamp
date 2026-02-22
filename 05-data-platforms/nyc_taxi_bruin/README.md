# NYC Taxi Pipeline (Bruin)

Bruin project for Module 5 homework (Data Platforms).

## Quick start

```powershell
bruin validate .\pipeline\pipeline.yml
bruin run .\pipeline\pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01
bruin lineage .\pipeline\pipeline.yml
```

## Structure

- `pipeline/assets/ingestion` - raw ingestion (Python + seed)
- `pipeline/assets/staging` - cleaned incremental table
- `pipeline/assets/reports` - daily aggregated report

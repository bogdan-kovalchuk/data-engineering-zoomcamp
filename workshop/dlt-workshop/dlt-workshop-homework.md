# dlt Workshop Homework (Local Notes / Answers Template)

Source instructions: `workshops/dlt_homework.md`

This version is prepared for local execution with the ready environment in `workshops/dlt-workshop/`.

## Setup status

- [ ] Virtual environment created
- [ ] Dependencies installed (`setup/requirements.txt`)
- [ ] Pipeline executed (`python taxi_pipeline.py`)
- [ ] Dashboard checked (`dlt pipeline taxi_pipeline show`)
- [ ] Answers verified (`python analysis.py` or `sql/homework_queries.sql`)

## Commands used

```powershell
cd workshops\dlt-workshop
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\setup\requirements.txt
python .\taxi_pipeline.py
python .\analysis.py
```

## Homework Questions (from workshop)

### Question 1: What is the start date and end date of the dataset?

- [ ] 2009-01-01 to 2009-01-31
- [ ] 2009-06-01 to 2009-07-01
- [ ] 2024-01-01 to 2024-02-01
- [ ] 2024-06-01 to 2024-07-01

Your answer:

```text
TODO
```

### Question 2: What proportion of trips are paid with credit card?

- [ ] 16.66%
- [ ] 26.66%
- [ ] 36.66%
- [ ] 46.66%

Your answer:

```text
TODO
```

### Question 3: What is the total amount of money generated in tips?

- [ ] $4,063.41
- [ ] $6,063.41
- [ ] $8,063.41
- [ ] $10,063.41

Your answer:

```text
TODO
```

## Notes

- API is paginated, 1000 rows per page, stop on empty page
- Pipeline file: `taxi_pipeline.py`
- SQL queries: `sql/homework_queries.sql`
- Helper analysis script: `analysis.py`

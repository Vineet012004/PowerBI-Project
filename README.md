# Healthcare Analytics & Risk Dashboard

A compact, end-to-end portfolio project that turns synthetic hospital encounter data into PostgreSQL analytics and a Power BI dashboard. It demonstrates Pandas data quality checks, normalized SQL, analytic queries, indexing, and clear KPI design.

> **Privacy note:** every record is synthetic. This project is for analytics demonstration only and must not be used for clinical decisions.

## What it demonstrates

- Python/Pandas: reproducible data generation, cleaning, validation, and feature engineering
- PostgreSQL: normalized operational schema, foreign keys, constraints, indexes, views, and analytical SQL
- SQL: JOINs, CTEs, window functions, subqueries, aggregations, and `CASE WHEN`
- Power BI: star-schema reporting view, Power Query import, DAX KPIs, drill-down friendly visuals

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\generate_sample_data.py
python src\transform_data.py
```

For PostgreSQL, create a database named `healthcare_analytics`, then run `sql/01_schema.sql`, `sql/02_load_csv.sql`, and `sql/03_analytics.sql` using `psql`. Update the absolute CSV paths at the top of the load script.

For the report, follow [docs/powerbi_build_guide.md](docs/powerbi_build_guide.md): import the CSVs in `data/powerbi/`, create the relationships, and paste measures from `powerbi/dax_measures.md`.

## Layout

```
data/raw/          Generated source extract with intentional data-quality issues
data/processed/    Clean relational load files
data/powerbi/      Star-schema CSVs for Power BI
src/               Generation and Pandas transformation scripts
sql/               Schema, load script, and analytical SQL
powerbi/           DAX measures
docs/              Data dictionary, dashboard guide, business insights
```

## Sources and design references

- [Microsoft: star schema guidance for Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- [Microsoft: dimensional-model-to-report tutorial](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dimensional-model-report)
- [PostgreSQL: CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
- [PostgreSQL: window expressions](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)

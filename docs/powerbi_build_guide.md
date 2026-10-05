# Power BI build guide

## Import and model

1. In **Get Data > Text/CSV**, load all five files from `data/powerbi/`.
2. In Power Query, set `admission_date`, `discharge_date`, and `date` to Date; `treatment_cost` to Fixed decimal; `length_of_stay` to Whole number. Close & Apply.
3. In Model view, create these one-to-many, single-direction relationships:

| From (1) | To (*) | Key |
|---|---|---|
| dim_date | fact_admissions | date → admission_date |
| dim_patient | fact_admissions | patient_id |
| dim_department | fact_admissions | department |
| dim_diagnosis | fact_admissions | diagnosis |

Mark `dim_date` as the date table using `date`. This is a simple star schema: dimensions filter the fact table, and fact rows remain at one-admission-per-row grain.

## Report pages

### 1. Executive overview

- Cards: Total Admissions, Total Treatment Cost, Average Length of Stay, Readmission Rate
- Line chart: `dim_date[year_month]` by Total Admissions
- Clustered bar: department by Total Treatment Cost
- Donut: outcome by Total Admissions
- Slicers: year, department, payer_type, severity

### 2. Risk and outcomes

- Matrix: age_band × department with Readmission Rate and Elevated Risk Rate
- Bar chart: diagnosis by Readmissions (sort descending)
- Scatter: department, X = Average Length of Stay, Y = Readmission Rate, Size = Total Admissions
- Table: diagnosis, Total Admissions, Average Length of Stay, Cost per Admission, Readmission Rate

### 3. Cost and operations

- Waterfall: department by Total Treatment Cost
- Line and clustered column: year_month, columns = Total Admissions, line = Average Length of Stay
- Decomposition tree: Total Treatment Cost by department → diagnosis → payer_type

Use the measures in `powerbi/dax_measures.md`. Add a tooltip page with Total Admissions, Cost per Admission, and Readmission Rate for richer departmental hover details.

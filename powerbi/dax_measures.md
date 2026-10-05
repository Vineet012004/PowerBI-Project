# DAX measures

Create these as measures on `fact_admissions`. Format currency measures as Currency and rates as Percentage.

```DAX
Total Admissions = COUNTROWS(fact_admissions)

Total Treatment Cost = SUM(fact_admissions[treatment_cost])

Average Length of Stay = AVERAGE(fact_admissions[length_of_stay])

Readmissions = CALCULATE([Total Admissions], fact_admissions[readmitted_30d] = "Yes")

Readmission Rate = DIVIDE([Readmissions], [Total Admissions])

Elevated Risk Admissions = CALCULATE([Total Admissions], fact_admissions[risk_flag] = "Elevated")

Elevated Risk Rate = DIVIDE([Elevated Risk Admissions], [Total Admissions])

Cost per Admission = DIVIDE([Total Treatment Cost], [Total Admissions])

Discharged Admissions = CALCULATE([Total Admissions], fact_admissions[outcome] = "Discharged")

Discharge Rate = DIVIDE([Discharged Admissions], [Total Admissions])

Admissions Previous Month =
CALCULATE([Total Admissions], DATEADD(dim_date[date], -1, MONTH))

Admissions MoM Change = [Total Admissions] - [Admissions Previous Month]

Admissions MoM % = DIVIDE([Admissions MoM Change], [Admissions Previous Month])
```

"""Clean source data and export normalized PostgreSQL and Power BI files."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "healthcare_encounters_raw.csv"
PROCESSED, POWERBI = ROOT / "data" / "processed", ROOT / "data" / "powerbi"
PROCESSED.mkdir(parents=True, exist_ok=True)
POWERBI.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(RAW, parse_dates=["admission_date", "discharge_date"])
raw_count = len(df)
df = df.drop_duplicates(subset="encounter_id").copy()
df["gender"] = df["gender"].str.strip().str.title()
df["department"] = df["department"].replace({"ER": "Emergency"})
df["treatment_cost"] = df.groupby("department")["treatment_cost"].transform(lambda s: s.fillna(s.median()))
df["length_of_stay"] = (df["discharge_date"] - df["admission_date"]).dt.days
df["age_band"] = pd.cut(df["age"], [0, 34, 49, 64, 200], labels=["18-34", "35-49", "50-64", "65+"])
df["risk_flag"] = ((df["severity"] == "High") | (df["age"] >= 65) | (df["length_of_stay"] >= 6)).map({True: "Elevated", False: "Standard"})
assert df.encounter_id.is_unique and (df.length_of_stay >= 0).all() and (df.treatment_cost > 0).all()
dim_patient = df[["patient_id", "age", "gender", "region", "age_band"]].drop_duplicates("patient_id").sort_values("patient_id")
dim_department = pd.DataFrame({"department": sorted(df.department.unique())})
dim_diagnosis = pd.DataFrame({"diagnosis": sorted(df.diagnosis.unique())})
fact = df[["encounter_id", "patient_id", "admission_date", "discharge_date", "department", "diagnosis", "severity", "payer_type", "treatment_cost", "outcome", "readmitted_30d", "length_of_stay", "risk_flag"]].sort_values("encounter_id")
for name, table in {"patients": dim_patient, "departments": dim_department, "diagnoses": dim_diagnosis, "admissions": fact}.items(): table.to_csv(PROCESSED / f"{name}.csv", index=False)
date_range = pd.date_range(fact.admission_date.min(), fact.admission_date.max(), freq="D")
dim_date = pd.DataFrame({"date": date_range})
dim_date["year"], dim_date["month_number"] = dim_date.date.dt.year, dim_date.date.dt.month
dim_date["month"], dim_date["year_month"] = dim_date.date.dt.strftime("%b"), dim_date.date.dt.strftime("%Y-%m")
dim_date["quarter"] = "Q" + dim_date.date.dt.quarter.astype(str)
for name, table in {"dim_date": dim_date, "dim_patient": dim_patient, "dim_department": dim_department, "dim_diagnosis": dim_diagnosis, "fact_admissions": fact}.items(): table.to_csv(POWERBI / f"{name}.csv", index=False)
quality = pd.DataFrame([{"raw_rows": raw_count, "clean_rows": len(df), "duplicates_removed": raw_count - len(df), "null_costs_after_cleaning": int(df.treatment_cost.isna().sum())}])
quality.to_csv(PROCESSED / "data_quality_summary.csv", index=False)
print(quality.to_string(index=False))

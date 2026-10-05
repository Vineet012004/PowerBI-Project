"""Generate a deterministic, fully synthetic healthcare encounter extract."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "healthcare_encounters_raw.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

N_PATIENTS, N_ENCOUNTERS = 800, 3_200
departments = {"Cardiology": .12, "Emergency": .30, "General Medicine": .24, "Oncology": .10, "Orthopedics": .12, "Pulmonology": .12}
diagnoses = {
    "Cardiology": ["Heart Failure", "Hypertension", "Arrhythmia"], "Emergency": ["Injury", "Infection", "Abdominal Pain"],
    "General Medicine": ["Diabetes", "Kidney Disease", "Dehydration"], "Oncology": ["Breast Cancer", "Lung Cancer", "Lymphoma"],
    "Orthopedics": ["Hip Fracture", "Arthritis", "Back Pain"], "Pulmonology": ["Pneumonia", "COPD", "Asthma"],
}
patient_ids = [f"P{i:05d}" for i in range(1, N_PATIENTS + 1)]
patients = pd.DataFrame({"patient_id": patient_ids, "age": rng.integers(18, 91, N_PATIENTS), "gender": rng.choice(["Female", "Male", "Non-binary"], N_PATIENTS, p=[.49, .49, .02]), "region": rng.choice(["North", "South", "East", "West"], N_PATIENTS)})
admit_dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 730, N_ENCOUNTERS), unit="D")
dept_names, dept_probs = list(departments), list(departments.values())
encounter_depts = rng.choice(dept_names, N_ENCOUNTERS, p=dept_probs)
base_los = {"Cardiology": 4.5, "Emergency": 2.2, "General Medicine": 4, "Oncology": 5.2, "Orthopedics": 4.2, "Pulmonology": 3.8}
base_cost = {"Cardiology": 15500, "Emergency": 7200, "General Medicine": 9200, "Oncology": 24000, "Orthopedics": 18000, "Pulmonology": 10500}
rows = []
for idx, (admit, dept) in enumerate(zip(admit_dates, encounter_depts), 1):
    patient = patients.iloc[rng.integers(0, N_PATIENTS)]
    age, severity = int(patient.age), rng.choice(["Low", "Medium", "High"], p=[.28, .50, .22])
    los = max(1, int(round(rng.normal(base_los[dept] + (2 if severity == "High" else 0), 1.5))))
    cost = max(500, round(rng.normal(base_cost[dept] * (1 + .20 * (severity == "High")), base_cost[dept] * .18), 2))
    readmit_probability = .07 + .10 * (severity == "High") + .05 * (age >= 65) + .04 * (los >= 6)
    outcome = rng.choice(["Discharged", "Transferred", "Deceased"], p=[.92, .06, .02])
    rows.append({"encounter_id": f"E{idx:06d}", "patient_id": patient.patient_id, "age": age, "gender": patient.gender, "region": patient.region, "admission_date": admit.date(), "discharge_date": (admit + pd.Timedelta(days=los)).date(), "department": dept, "diagnosis": rng.choice(diagnoses[dept]), "severity": severity, "payer_type": rng.choice(["Private", "Medicare", "Medicaid", "Self-pay"], p=[.43, .31, .20, .06]), "treatment_cost": cost, "outcome": outcome, "readmitted_30d": "Yes" if rng.random() < readmit_probability and outcome == "Discharged" else "No"})

df = pd.DataFrame(rows)
# Intentional source-quality issues for the cleaning pipeline to resolve.
df.loc[df.sample(frac=.01, random_state=SEED).index, "gender"] = " female "
df.loc[df.sample(frac=.008, random_state=SEED + 1).index, "treatment_cost"] = np.nan
df.loc[df.sample(frac=.004, random_state=SEED + 2).index, "department"] = "ER"
df = pd.concat([df, df.head(8)], ignore_index=True)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df):,} raw rows to {OUT}")

# Data dictionary

| Field | Meaning |
|---|---|
| encounter_id | Unique synthetic hospital encounter identifier |
| patient_id | De-identified synthetic patient identifier |
| admission_date / discharge_date | Encounter start and end dates |
| department / diagnosis | Treating service and primary diagnosis group |
| severity | Low, Medium, or High source severity classification |
| treatment_cost | Synthetic total treatment cost in USD |
| outcome | Discharged, Transferred, or Deceased |
| readmitted_30d | Synthetic readmission indicator within 30 days |
| length_of_stay | Days between admission and discharge |
| risk_flag | Elevated if high severity, age 65+, or stay of 6+ days |

The raw extract deliberately contains duplicate encounter rows, inconsistent `gender` and `department` labels, and missing costs. `src/transform_data.py` documents and resolves each issue.

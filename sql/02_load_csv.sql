-- Run 01_schema.sql first. Change this path to your local processed-data folder.
SET search_path TO healthcare;
\copy patients FROM 'C:/Users/dscsa/Desktop/power_BI_project/data/processed/patients.csv' WITH (FORMAT csv, HEADER true)
\copy departments FROM 'C:/Users/dscsa/Desktop/power_BI_project/data/processed/departments.csv' WITH (FORMAT csv, HEADER true)
\copy diagnoses FROM 'C:/Users/dscsa/Desktop/power_BI_project/data/processed/diagnoses.csv' WITH (FORMAT csv, HEADER true)
\copy admissions FROM 'C:/Users/dscsa/Desktop/power_BI_project/data/processed/admissions.csv' WITH (FORMAT csv, HEADER true)
ANALYZE healthcare.admissions;

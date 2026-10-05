-- Normalized PostgreSQL operational model (synthetic data only)
DROP SCHEMA IF EXISTS healthcare CASCADE;
CREATE SCHEMA healthcare;
SET search_path TO healthcare;

CREATE TABLE patients (
    patient_id VARCHAR(10) PRIMARY KEY,
    age SMALLINT NOT NULL CHECK (age BETWEEN 0 AND 120),
    gender VARCHAR(20) NOT NULL,
    region VARCHAR(20) NOT NULL,
    age_band VARCHAR(10) NOT NULL
);
CREATE TABLE departments (department VARCHAR(50) PRIMARY KEY);
CREATE TABLE diagnoses (diagnosis VARCHAR(80) PRIMARY KEY);
CREATE TABLE admissions (
    encounter_id VARCHAR(12) PRIMARY KEY,
    patient_id VARCHAR(10) NOT NULL REFERENCES patients(patient_id),
    admission_date DATE NOT NULL,
    discharge_date DATE NOT NULL CHECK (discharge_date >= admission_date),
    department VARCHAR(50) NOT NULL REFERENCES departments(department),
    diagnosis VARCHAR(80) NOT NULL REFERENCES diagnoses(diagnosis),
    severity VARCHAR(10) NOT NULL CHECK (severity IN ('Low','Medium','High')),
    payer_type VARCHAR(20) NOT NULL,
    treatment_cost NUMERIC(12,2) NOT NULL CHECK (treatment_cost > 0),
    outcome VARCHAR(20) NOT NULL,
    readmitted_30d VARCHAR(3) NOT NULL CHECK (readmitted_30d IN ('Yes','No')),
    length_of_stay SMALLINT NOT NULL CHECK (length_of_stay >= 0),
    risk_flag VARCHAR(10) NOT NULL
);

-- Target frequent filtering and join paths. Validate with EXPLAIN (ANALYZE, BUFFERS).
CREATE INDEX idx_admissions_date ON admissions (admission_date);
CREATE INDEX idx_admissions_department_date ON admissions (department, admission_date);
CREATE INDEX idx_admissions_patient ON admissions (patient_id);
CREATE INDEX idx_admissions_readmission ON admissions (readmitted_30d) WHERE readmitted_30d = 'Yes';

-- Reporting-friendly denormalized view; operational source remains normalized above.
CREATE VIEW vw_admission_analytics AS
SELECT a.*, p.age, p.gender, p.region, p.age_band
FROM admissions a JOIN patients p USING (patient_id);

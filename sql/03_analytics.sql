SET search_path TO healthcare;

-- 1) KPI roll-up: aggregations + CASE WHEN
SELECT department,
       COUNT(*) AS admissions,
       ROUND(SUM(treatment_cost), 2) AS total_cost,
       ROUND(AVG(length_of_stay), 2) AS avg_los,
       ROUND(100.0 * AVG(CASE WHEN readmitted_30d = 'Yes' THEN 1 ELSE 0 END), 2) AS readmission_rate_pct
FROM admissions
GROUP BY department ORDER BY total_cost DESC;

-- 2) CTE + JOIN: monthly operational trend
WITH monthly AS (
  SELECT date_trunc('month', admission_date)::date AS month, department,
         COUNT(*) AS admissions, SUM(treatment_cost) AS cost
  FROM admissions GROUP BY 1, 2
)
SELECT month, department, admissions, ROUND(cost, 2) AS total_cost,
       ROUND(100.0 * cost / SUM(cost) OVER (PARTITION BY month), 2) AS monthly_cost_share_pct
FROM monthly ORDER BY month, total_cost DESC;

-- 3) Window function: rank diagnosis costs within department
SELECT department, diagnosis, COUNT(*) AS admissions, ROUND(SUM(treatment_cost), 2) AS total_cost,
       DENSE_RANK() OVER (PARTITION BY department ORDER BY SUM(treatment_cost) DESC) AS cost_rank
FROM admissions
GROUP BY department, diagnosis ORDER BY department, cost_rank;

-- 4) Correlated subquery: encounters exceeding their department's average length of stay
SELECT a.encounter_id, a.department, a.diagnosis, a.length_of_stay
FROM admissions a
WHERE a.length_of_stay > (
  SELECT AVG(b.length_of_stay) FROM admissions b WHERE b.department = a.department
)
ORDER BY a.department, a.length_of_stay DESC;

-- 5) Patient-level risk cohort with multiple joins
SELECT p.age_band, p.region, d.department,
       COUNT(*) AS admissions,
       ROUND(100.0 * AVG(CASE WHEN a.risk_flag = 'Elevated' THEN 1 ELSE 0 END), 1) AS elevated_risk_pct,
       ROUND(100.0 * AVG(CASE WHEN a.readmitted_30d = 'Yes' THEN 1 ELSE 0 END), 1) AS readmission_rate_pct
FROM admissions a
JOIN patients p ON p.patient_id = a.patient_id
JOIN departments d ON d.department = a.department
GROUP BY p.age_band, p.region, d.department
HAVING COUNT(*) >= 10
ORDER BY readmission_rate_pct DESC, admissions DESC;

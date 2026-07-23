-- Model 2: Department summary
-- references employees_cleaned model

SELECT
    department,
    COUNT(*)              AS employee_count,
    ROUND(AVG(salary), 0) AS avg_salary,
    MAX(salary)           AS max_salary,
    MIN(salary)           AS min_salary,
    SUM(salary)           AS total_salary_cost
FROM {{ ref('employees_cleaned') }}
GROUP BY department
ORDER BY avg_salary DESC

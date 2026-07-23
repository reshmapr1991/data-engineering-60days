-- Model 1: Clean employee data

SELECT
    emp_id,
    name,
    department,
    salary,
    city,
    joining_date,
    EXTRACT(YEAR FROM CURRENT_DATE) - 
    EXTRACT(YEAR FROM joining_date::date) AS experience_years,
    CASE
        WHEN salary >= 90000 THEN 'Grade A'
        WHEN salary >= 80000 THEN 'Grade B'
        WHEN salary >= 70000 THEN 'Grade C'
        ELSE 'Grade D'
    END AS salary_grade
FROM employees1
WHERE salary > 0

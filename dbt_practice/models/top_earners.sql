-- Model 3: Top earner per department
-- references employees_cleaned model

SELECT
    name,
    department,
    salary,
    salary_grade,
    experience_years
FROM (
    SELECT
        name,
        department,
        salary,
        salary_grade,
        experience_years,
        RANK() OVER (
            PARTITION BY department
            ORDER BY salary DESC
        ) AS dept_rank
    FROM {{ ref('employees_cleaned') }}
) ranked
WHERE dept_rank = 1
ORDER BY salary DESC

employees = [
    {"name": "Ravi",   "department": "Engineering", "salary": 90000},
    {"name": "Priya",  "department": "Marketing",   "salary": 75000},
    {"name": "Arjun",  "department": "Engineering", "salary": 85000},
    {"name": "Sneha",  "department": "HR",          "salary": 60000},
    {"name": "Karan",  "department": "Marketing",   "salary": 70000},
    {"name": "Meera",  "department": "HR",          "salary": 65000},
]

# Step 1: group by department
dept_salaries = {}
for emp in employees:
    dept = emp["department"]
    if dept not in dept_salaries:
        dept_salaries[dept] = []
    dept_salaries[dept].append(emp["salary"])

print(dept_salaries)

# Step 2: calculate averages
print("=" * 40)
print("Department Salary Report")
print("=" * 40)
for dept, salaries in dept_salaries.items():
    avg = sum(salaries) / len(salaries)
    print(f"{dept:<15} Avg Salary: ₹{avg:,.0f}")

    # Step 3: find highest paying dept
    top_dept = max(dept_salaries, key=lambda d: sum(dept_salaries[d]) / len(dept_salaries[d]))
    print(f"\nHighest paying department: {top_dept}")
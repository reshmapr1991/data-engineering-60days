import csv
import json

# Read CSV manually (before pandas)
with open("empl.csv", "r") as f:
    reader = csv.DictReader(f)
    employees = list(reader)

print(f"Total employees: {len(employees)}")
for emp in employees:
    print(f"{emp['name']} works in {emp['department']} earning {emp['salary']}")

# Filter: only Engineering employees
engineers = [e for e in employees if e["department"] == "Engineering"]
print(f"\nEngineers: {len(engineers)}")

# Write filtered results to a new CSV
with open("engineers_only.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "department", "salary"])
    writer.writeheader()
    writer.writerows(engineers)
print("Saved engineers_only.csv")

# JSON read/write
data = {"date": "2024-01-01", "records": len(employees)}
with open("empl1.json", "w") as f:
    json.dump(data, f, indent=2)
print("Saved summary.json")

with open("empl1.json", "r") as f:
    loaded = json.load(f)
print(f"Loaded JSON: {loaded}")
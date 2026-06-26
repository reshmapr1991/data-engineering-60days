import pandas as pd
import datetime

print("="*40)
print("ETL Pipeline Running in Docker!")
print(f"Time: {datetime.datetime.now()}")
print("="*40)

# create sample data
data = {
    "name":       ["Rahul", "Priya", "Arjun"],
    "department": ["Engineering", "Marketing", "HR"],
    "salary":     [90000, 75000, 60000]
}

df = pd.DataFrame(data)

# transform
df["salary_usd"] = (df["salary"] / 83).round(0)
df["grade"] = df["salary"].apply(
    lambda x: "A" if x >= 80000 else "B" if x >= 70000 else "C"
)

print("\nProcessed Data:")
print(df.to_string(index=False))
print("\nDepartment Summary:")
print(df.groupby("department")["salary"].mean().round(0))
print("\nETL Complete!")

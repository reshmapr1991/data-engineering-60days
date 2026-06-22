import pandas as pd
import numpy as np

# Simulate a messy real-world dataset
messy_data = {
    "emp_id":     [101, 102, 103, 104, 105, 102],   # 102 is duplicate
    "name":       ["Ravi", "  priya ", "ARJUN", None, "Karan", "Priya"],
    "department": ["Engineering", "marketing", "Engineering", "HR", None, "Marketing"],
    "salary":     [90000, 75000, None, 60000, -5000, 75000],  # None and negative
    "email":      ["ravi@co.com", "priya@co.com", "arjun@co.com", "sneha@co.com", "bad-email", "priya@co.com"]
}

df = pd.DataFrame(messy_data)
print("Raw messy data:\n", df)
print("\nNull counts:\n", df.isnull().sum())

# Step 1: remove duplicates
df = df.drop_duplicates(subset=["emp_id"])
print(f"\nAfter removing duplicates: {len(df)} rows")

# Step 2: fix null values
df["salary"]     = df["salary"].fillna(df["salary"].median())
df["department"] = df["department"].fillna("Unknown")
df = df.dropna(subset=["name"])   # drop rows where name is missing

# Step 3: standardise strings
df["name"]       = df["name"].str.strip().str.title()
df["department"] = df["department"].str.strip().str.title()

# Step 4: fix invalid values
df = df[df["salary"] > 0]   # remove negative salaries

# Step 5: validate email format (basic check)
df["email_valid"] = df["email"].str.contains(r"@.*\.", regex=True)
print("\nEmail validation:\n", df[["name", "email", "email_valid"]])

print("\nCleaned data:\n", df)
print("\nFinal shape:", df.shape)
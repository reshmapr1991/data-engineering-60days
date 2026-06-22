import pandas as pd

#load data
df = pd.read_csv("prac2.csv")

#dropduplicates
df =df.drop_duplicates(subset =["patient_id"])

#clean names
df["name"]=df["name"].str.strip().str.title()

#missing age
df =df.dropna(subset=["age"])

#negative age
df=df[df["age"] > 0]

#impossible age
df = df[df["age"] < 120]



#invalid blood type
valid_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
df["blood_type_valid"] = df["blood_type"].isin(valid_types)
df = df[df["blood_type_valid"] == True]

#invalid gender
df["gender"] =df["gender"].replace("MALE","M")

#discharge date missing so parsing data
df["admission_date"]     = pd.to_datetime(df["admission_date"], errors="coerce")
df["discharge_date"]     = pd.to_datetime(df["discharge_date"], errors="coerce")
df["stay_duration_days"] = (df["discharge_date"] - df["admission_date"]).dt.days

#flag cost of patients
df["high_cost"] = df["treatment_cost"] > 200000

# look at P001 and P015 side by side
suspects = df[df["name"] == "Rahul Sharma"]
print(suspects[["patient_id", "name", "age", "gender", "blood_type",
                 "city", "doctor", "admission_date", "diagnosis"]])

# find duplicates based on personal details (not patient_id)
duplicate_mask = df.duplicated(
    subset=["name", "age", "city", "blood_type"],
    keep="first"   # keep the first record, flag the rest
)

print(f"Suspected duplicate persons: {duplicate_mask.sum()}")
print(df[duplicate_mask][["patient_id", "name", "age", "city"]])

# remove them
df = df[~duplicate_mask]
print(f"Rows after removing person duplicates: {len(df)}")

print("\n" + "="*40)
print("     Cleaning Report")
print("="*40)
print(f"Rows after cleaning       : {len(df)}")
print(f"Still admitted patients   : {df['discharge_date'].isna().sum()}")
print(f"High cost treatments      : {df['high_cost'].sum()}")
print(f"\nNull counts:\n{df.isnull().sum()}")
print("="*40)


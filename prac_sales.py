import pandas as pd

df= pd.read_csv("prac3_sales.csv")
df1=pd.read_csv("prac3_managers.csv")
print(df)
print(df1)

print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nFirst 5:\n", df.head())
print("\nNulls:\n", df.isnull().sum())

import pandas as pd

# Load the data
df = pd.read_csv('prac3_sales.csv')

# 1. Check for missing values
print("Missing values per column:")
print(df.isnull().sum())

# 2. Remove duplicate rows
df = df.drop_duplicates()

# 3. Handle missing values (if any existed)
# Option A: Drop rows with any missing values
df = df.dropna()

# Option B: Fill missing values with appropriate defaults
# df['sales_amount'].fillna(0, inplace=True)
# df['name'].fillna('Unknown', inplace=True)

# 4. Remove negative values in numeric columns
df = df[(df['sales_amount'] >= 0) & (df['target'] >= 0)]

# 5. Standardize text columns (lowercase, strip whitespace)
df['name'] = df['name'].str.strip().str.lower()
df['region'] = df['region'].str.strip()
df['team'] = df['team'].str.strip()

# 6. Convert date column to proper datetime format
df['joining_date'] = pd.to_datetime(df['joining_date'])

# 7. Remove outliers (optional - using IQR method)
Q1 = df['sales_amount'].quantile(0.25)
Q3 = df['sales_amount'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['sales_amount'] >= Q1 - 1.5*IQR) &
        (df['sales_amount'] <= Q3 + 1.5*IQR)]

# 8. Check for duplicate employee-quarter combinations
df = df.drop_duplicates(subset=['emp_id', 'quarter'], keep='first')

# 9. Validate data ranges
df = df[(df['rating'] >= 0) & (df['rating'] <= 5)]
df = df[df['experience_years'] >= 0]

# Save cleaned data
df.to_csv('cleaned_sales_data.csv', index=False)

print(f"\nCleaned data shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())


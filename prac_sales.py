import pandas as pd

df= pd.read_csv("prac3_sales.csv")
df1=pd.read_csv("prac3_managers.csv")
print(df)
print(df1)

print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nFirst 5:\n", df.head())
print("\nNulls:\n", df.isnull().sum())


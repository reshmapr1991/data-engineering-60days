from importlib.readers import remove_duplicates

import numpy as np
import pandas as pd

product_category = {
    "Laptop": "Electronics",
    "Shoes": "Fashion",
    "Rice": "Grocery"
}
products = np.random.choice(list(product_category.keys()), 500)
categories = [product_category[product] for product in products]
def gen1():
    df=pd.DataFrame({
        "Order_ID":[i for i in range(1001,1501)],
        "Customer_ID":([f"C{i}" for i in  np.random.randint(100,300,500)]),
        "Product": products,
        "Category": categories,
        'Quantity': np.random.randint(1, 6, 500),
        'Price':np.random.randint(100,5000,500),
        'Order_date':np.random.choice(pd.date_range('2024-01-01','2024-12-31'),500),
        'Payment_mode':np.random.choice(['UPI','Card','Cash','Net Banking','Crypto','Cheque'],500)
        })
    return df

df=gen1()

#1st 10 records
print(df.head(10))

#Last 10 records
print(df.tail(10))

#shape of df
print(df.shape)

#No.of orders for each payment mode
count_orders=df["Payment_mode"].value_counts()
print(f"Count of orders for each payment mode : {count_orders}")

#datatypes
df.info()

#Average price
df['average_price'] = round(df['Price'].mean(),2)
print(f"Average price:\n {df['average_price']}")

#Highest price order
print(df.loc[df["Price"].idxmax()])

#Lowest price order
print(df[df["Price"] == df["Price"].min()])

#total amount
df["Total_Amount"] = df["Quantity"]* df["Price"]
#print(f"Total Amount is:{Total_Amount}")

#discount
discount_products ={
                    "Electronics" :0.10,
                    "Fashion" : 0.5,
                    "Grocery" : 0.2
                    }
discount= df['Category'].map(discount_products)
df['Discount'] = df['Total_Amount'] * discount
df['Discounted_amount'] =df["Total_Amount"] - df['Discount']

#Calculate GST
gst_calc={
    'Electronics' : 0.18,
    'Fashion' : 0.12,
    'Grocery' : 0.5
}

df['GST'] =df['Discounted_amount'] * df['Category'].map(gst_calc)
df['Net_Amount'] =df['GST'] + df['Discounted_amount']

#Total sales
print(f"Total Sales:{df['Net_Amount'].sum()}")

#Average order value
order_totals = df.groupby('Order_ID')['Price'].sum()

# Average Order Value
aov = order_totals.mean()
print(f"Average order value: {aov}")

#Most frequently purchased product
most_frequent = df['Product'].value_counts().idxmax()
print(most_frequent)

#Most popular payment mode
count = df['Payment_mode'].max()
print(count)

#Highest revenue category
# highest_revenue = df.groupby("Category")["Revenue"].max()
# print(highest_revenue)

#Sort the dataset by Order_Date
df.sort_values('Order_date')
print("Sorted")


# #Price (descending)
sorted_df =df.sort_values("Price",ascending=False)
print(sorted_df)

#save sorted_df
sorted_df.to_csv("sorted_orders.csv",index=False)

#10 rows with missing Price
null_price =df['Price'].isna().sum()
print(null_price)

#5 duplicate records
duplicate_records =df.duplicated().sum()
print(duplicate_records)

#8 rows with invalid Payment_Mode values (e.g., "Crypto", "Cheque")
filtered_payment = df[df['Payment_mode'].isin(['Crypto', 'Cheque'])]
filtered_columns = filtered_payment.filter(items=['Order_ID', 'Payment_mode', 'Price'])

print(filtered_columns)

#Detect missing values
missing_values=df.isna().values.any()
print(missing_values)

#remove duplicates
remove_duplicates = df.drop_duplicates()
print(f"duplicates removed :{remove_duplicates}")

#Replace invalid payment modes with "Unknown"
valid_modes = ['Cash', 'Card', 'UPI', 'Cheque', 'Net Banking']

df['Payment_mode'] = df['Payment_mode'].where(
    df['Payment_mode'].isin(valid_modes),
    'Unknown'
)

#Extract date features
df['Year'] = df['Order_date'].dt.year
df['Month'] = df['Order_date'].dt.month
df['Day'] = df['Order_date'].dt.day
df['Quarter_Num'] = df['Order_date'].dt.quarter
df['day_number'] = df['Order_date'].dt.dayofweek
df['day_name'] = df['Order_date'].dt.day_name()

week_day =['Monday','Tuesday','Wednesday','Thursday','Friday']
week_end=['Saturday','Sunday']
df['day_name'] =df['day_name'].where(df['day_name'].isin(week_end),'Week day')
df['day_name'] = df['day_name'].replace({
    'Saturday':'Week end',
    'Sunday':'Week end'
})
print(df)

#Categorize Orders
# Price <500 Cheap
# 500–2000 Medium
#>2000 Premium
df['Categorize'] =df['Price'].replace({
    ''
})





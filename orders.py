import numpy as np
import pandas as pd
product_category = { "Laptop": "Electronics", "Shoes": "Fashion", "Rice": "Grocery" }
products = np.random.choice(list(product_category.keys()), 500)
categories = [product_category[product] for product in products]
def gen1():
    df=pd.DataFrame({
        "Order_ID":[i for i in range(1001,1501)],
        "Customer_ID":([f"C{i}" for i in np.random.randint(100,300,500)]),
        "Product": products,
        "Category": categories,
        'Quantity': np.random.randint(1, 5, 500),
        'Price':np.random.randint(100,5000,500),
        'Order_date':np.random.choice(pd.date_range('2024-01-01','2024-12-31')),
        'Payment_mode':np.random.choice(['UPI','Card','Cash','Net Banking'],500) })
    return df
df=gen1()
print(df)
#1st 10 records
print(df.head(10))
# #Last 10 records
print(df.tail(10))
#shape of df
print(df.shape)
#No.of orders for each payment mode
count_orders=df["Payment_mode"].value_counts()
print(f"Count of orders for each payment mode : {count_orders}")
#datatypes
df.info()
#Average price
df['average_price'] = df['Price']/len(df['Order_ID'])
print(f"Average price:\n {df['average_price']}")
#Highest price order
print(df.sort_values("Price",ascending=False))
#Lowest price order
print(df.sort_values("Price",ascending=True))
# total
df['Total_Amount'] = df['Quantity']* df['Price']
#print(f"Total Amount is:{df['Total_Amount']}")
#discount
discount_products ={
                    "Electronics" :0.10,
                    "Fashion" : 0.5,
                    "Grocery" : 0.2
                    }
discount= df['Category'].map(discount_products)
df['Discount'] = df['Total_Amount'] * discount
#gst
gst_calc={
    'Electronics' : 0.18,
    'Fashion' : 0.12,
    'Grocery' : 0.5
}

df['GST'] =df['Discount'] * df['Category'].map(gst_calc)
df['Net Amount'] = df['GST'] + df['Discount']
print('Net Amount')
#order date
df.sort_values('Order_date')

# From Order_Date create
#
# Year
# Month
# Day
# Quarter
# Weekday
# Weekend (Yes/No)

df['year']=df['Order_date'].dt.year
df['month']=df['Order_date'].dt.month_name()
df['day']=df['Order_date'].dt.day_name()
df['quarter']=df['Order_date'].dt.quarter
# weekday =['Monday','Tuesday','Wednesday','Thursday','Friday']
# weekend =['Saturday','Sunday']
# df['Day_type']=np.where(df['day'].isin( weekday),"No","Yes")
df["day"] = df["day"].replace({
    "Monday": "Weekday",
    "Tuesday": "Weekday",
    "Wednesday": "Weekday",
    "Thursday": "Weekday",
    "Friday": "Weekday",
    "Saturday": "Weekend",
    "Sunday": "Weekend"
})

#Categorize Orders
# df['Categorize']=df['Price'].mask(df['Price']<500,'Cheap')
df.loc[df['Price'] < 500, 'Price_Category'] = 'Cheap'
df.loc[df['Price'] > 2000, 'Price_Category'] = 'Premium'
df.loc[(df['Price'] >=500) & (df['Price']<= 2000), 'Price_Category'] = 'Medium'

#monthly revenue
monthly_revenue = df.groupby("month",as_index=False)['Net Amount'].sum()
print(monthly_revenue)

#monthly order count
order_count=df.groupby("month")["Quantity"].sum()
print(order_count)

#Category-wise Revenue
category_report = df.groupby("Category").agg(
    Revenue=("Net Amount", "sum"),
    Average_Price=("Price", "mean"),
    Maximum_Price=("Price", "max"),
    Minimum_Price=("Price", "min")
)

print(category_report)

#Top 3 Orders Per Month
top_3_orders = df['Product'].rank(ascending=False)
print(top_3_orders)




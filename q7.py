import numpy as np
import pandas as pd

def generate_test_q7():
    df = pd.DataFrame({
        'Category': np.random.choice(['Electronics', 'Clothing', 'Home'], 30),
        'Product_ID': [f'P{i}' for i in range(1, 31)],
        'Price': np.random.randint(100, 1000, 30),
        'Quantity': np.random.randint(1, 20, 30),
        'Rating': np.random.choice([1, 2, 3, 4, 5], 30)

    })
    return df

def sales_total():
    df['Total_Sales'] = df['Price'] * df['Quantity']
    print(df.head())

    return df

# def cat_sales():
#     cat_sales = df.groupby('Category')['Total_Sales'].sum().reset_index()
#     print(cat_sales)

# def top_five():
#     top5 = df.sort_values('Total_Sales').head(5)
#     print(top5)

def rank_sales():
    df['Dense_Rank'] = (
        df.groupby('Category')['Total_Sales']
        .rank(method='dense', ascending=False)
    )

    print(df.head())


df = generate_test_q7()
df = sales_total()
#df = cat_sales()
#df = top_five()
df = rank_sales()
print(df)



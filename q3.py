import pandas as pd
import numpy as np

def generate_test_q3():
    df = pd.DataFrame({
        'User_ID': np.random.choice(['U1', 'U2', 'U3'], 30),
        'Date': pd.date_range(start='2023-01-01', periods=30),
        'Page_Views': np.random.randint(10, 500, 30)
    })
    return df

def add_date():
    df = pd.DataFrame({
        df['Day'] == df['Date'].dt.day,
        df['Month'] == df['Date'].dt.month,
        df['Year'] == df['Date'].dt.year


    })
    return df

def avg_page_views():
    user_avg = df.groupby('User_ID')['Page_Views'].mean().reset_index()
    return user_avg

df = generate_test_q3()
user_avg  = avg_page_views()

print(df)
print(user_avg)

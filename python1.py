import pandas as pd
import numpy as np

def generate_test_q1():
    df = pd.DataFrame({
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 20),
        'SalesPerson': [f"SP{i}" for i in range(1, 21)],
        'Revenue': np.random.randint(1000, 10000, 20)
    })
    return df
df =generate_test_q1()
print(df)



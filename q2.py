import pandas as pd
import numpy as np


def generate_test_q2():
    df = pd.DataFrame({
        'Department': np.random.choice(['HR', 'Finance', 'Tech', 'Marketing'], 15),
        'Employee': [f'Emp{i}' for i in range(1, 16)],
        'Salary': np.random.choice([50000, 60000, 70000, 80000, np.nan], 15)
    })
    return df
df=generate_test_q2()

print(df)

import pandas as pd
import numpy as np

def generate_test_q10():

   df = pd.DataFrame({
        'Feature1': np.append(np.random.normal(50, 10, 18), [150, 200]),
        'Feature2': np.append(np.random.normal(30, 5, 18), [100, 120])
    })
   return df

df = generate_test_q10()

print(df)




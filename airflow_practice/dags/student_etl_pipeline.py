from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import numpy as np
import os

default_args = {"owner": "tejas", "retries": 1}

DATA_DIR="/opt/airflow/dags/data"
def extract():

    df = pd.read_csv(f"{DATA_DIR}/students.csv")
    #print table
    print(df)

    #print first 5 rows
    print (f"Head: {df.head()}")

    #print shape
    print(f"Shape:{df.shape}")

    sum_null= df.isnull().sum().sum()
    print(f"Count of null:{sum_null}")

    df.to_csv(f"{DATA_DIR}/extracted.csv", index=False)
    print("Saved extracted.csv")

def clean_names():
    df = pd.read_csv(f"{DATA_DIR}/extracted.csv")

    # fixing spaces
    df["name"]= df["name"].str.strip()

    #capitalize name
    df["name"]=df["name"].str.title()

    #print before and after column of name
    print(df.iloc[:, :3])

    df.to_csv(f"{DATA_DIR}/names_cleaned.csv", index=False)
    print("Saved names_cleaned.csv")

def fix_nulls():
    df = pd.read_csv(f"{DATA_DIR}/names_cleaned.csv")
    print(f"Nulls BEFORE: {df.isnull().sum().sum()}")

    #fix nulls
    #math_score
    df["math_score"] = df["math_score"].fillna(df["math_score"].median())

    # english_score
    df["english_score"] = df["english_score"].fillna(df["english_score"].median())

    #science_score
    df["science_score"] = df["science_score"].fillna(df["science_score"].median())

    #count of null after
    sum_null = df.isnull().sum().sum()
    print(f"Count of null:{sum_null}")

    #create new column
    df["total_score"] = df["math_score"] + df["english_score"] + df["science_score"]

    #avg
    df["average_score"] = df["total_score"] / 3
    df["average_score"]  = df["average_score"] .round(1)

    df.to_csv(f"{DATA_DIR}/nulls_fixed.csv", index=False)
    print("Saved nulls_fixed.csv")

def add_columns():
    df = pd.read_csv(f"{DATA_DIR}/nulls_fixed.csv")
    #grade
    conditions= [df['average_score'] >= 85,
                df['average_score'] >= 70,
                df['average_score'] >= 55,
                df['average_score'] < 55
    ]
    choices=["A","B","C","D"]
    df['Grade'] = np.select(conditions, choices, default='F')
    print(df)
    count_grades =df['Grade'].value_counts()
    print(count_grades)
    df.to_csv(f"{DATA_DIR}/final.csv", index=False)
    print("Saved final.csv")

def analyse():
    df = pd.read_csv(f"{DATA_DIR}/final.csv")
    count_of_A = df[df["Grade"]== "A"]["Grade"].count()
    print(f"Count of students with A grade {count_of_A}")

    count_of_B = df[df["Grade"] == "B"]["Grade"].count()
    print(f"Count of students with B grade {count_of_B}")

    count_of_C = df[df["Grade"] == "C"]["Grade"].count()
    print(f"Count of students with C grade {count_of_C}")

    count_of_D = df[df["Grade"] == "D"]["Grade"].count()
    print(f"Count of students with D grade {count_of_D}")

    #highest total score
    highest_score= df.groupby("city")["average_score"].mean().idxmax()

    #attendence <70
    attend_count = df[df["attendance"]<70]
    print(f"attendance count < 70: {len(attend_count)}")
    print(attend_count)

    #pass rate
    pass_rate = (df["average_score"] >=55).sum() / len(df) * 100
    print(f"pass rate is:{pass_rate}")

    #generate report
    print("="*50)
    print("STUDENT PERFORMANCE REPORT".center(50))
    print("="*50)
    print(f"Total students:{len(df)}")
    status_active =df[df["status"]=="active"]
    print(f"Active Students:{len(status_active)}")
    status_inactive = df[df["status"] == "inactive"]
    print(f"Inactive students:{len(status_inactive)}")
    print("-"*50)
    print(f"Grade A students:{count_of_A}")
    print(f"Grade B students:{count_of_B}")
    print(f"Grade C students:{count_of_C}")
    print(f"Grade D students:{count_of_D}")
    print("-" * 50)
    max_score = df['total_score'].max()
    highest_score_city=df[df['total_score'] == max_score]['city']
    print(f"Highest scoring city:{highest_score}")
    #Average attendance
    average_attend =df["attendance"].mean()
    print(f"Average attendance :{average_attend}")
    print(f"Pass rate:{pass_rate :.1f}%")

# ── DAG ───────────────────────────────────────────────────────────────────────
with DAG(
    dag_id="student_etl_pipeline",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["practice", "students"],
) as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="clean_names", python_callable=clean_names)
    t3 = PythonOperator(task_id="fix_nulls", python_callable=fix_nulls)
    t4 = PythonOperator(task_id="add_columns", python_callable=add_columns)
    t5 = PythonOperator(task_id="analyse", python_callable=analyse)
    t1 >> t2 >> t3 >> t4 >> t5

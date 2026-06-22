import pandas as pd
import numpy as np


def generate_test_q6():
    df = pd.DataFrame({
        'User_ID': np.random.choice(['U1', 'U2', 'U3'], 25),
        'Action': np.random.choice(['Click', 'Scroll', 'Purchase'], 25),
        'Timestamp': pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 100, 25), unit='m')
    })
    return df
df = generate_test_q6()

# df_purchase = df.filter(df.Action == "Purchase")
# print(df_purchase)

#df_selected = df.select("User_ID", "Action")

#df_sorted = df.orderBy("Timestamp")


df_action_count = (
    df.groupby("User_ID")["Action"]
      .count()
      .reset_index(name="total_actions")
)

print(df_action_count)

#from pyspark.sql.functions import hour

#df_hour = df.withColumn("hour", hour("Timestamp"))

#from pyspark.sql.window import Window
#from pyspark.sql.functions import row_number

# w = Window.partitionBy("User_ID").orderBy("Timestamp")
#
# df_ranked = df.withColumn("action_order", row_number().over(w))
#
df_users = df["User_ID"].unique()

print(df_users)
#
# df_time = df.filter(df.Timestamp.between("2023-01-01 00:00:00", "2023-01-01 01:00:00"))
#
# df_pivot = df.groupBy("User_ID") \
#              .pivot("Action") \
#              .count()

#
# from pyspark.sql.functions import lag
# from pyspark.sql.functions import unix_timestamp
#
# w = Window.partitionBy("User_ID").orderBy("Timestamp")
#
# df_session = df.withColumn(
#         "prev_time",
#          lag("Timestamp").over(w)
#          ).withColumn(
#          "time_diff_sec",
#          unix_timestamp("Timestamp") - unix_timestamp("prev_time")
# )


import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import datetime
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

engine = create_engine(os.environ["DB_STRING"])

query_pos = """
SELECT C.tweet_id, C.DiffTimeStamp resp_time
FROM Conversations C
WHERE C.airline = "KLM"
AND C.sentiment_change = 1
AND C.user_id = 56377143
"""

query_neg = """
SELECT C.tweet_id, C.DiffTimeStamp resp_time
FROM Conversations C
WHERE C.airline = "KLM"
AND C.sentiment_change = -1
AND C.user_id = 56377143
"""

df_pos = pd.read_sql_query(query_pos, engine)
df_neg = pd.read_sql_query(query_neg, engine)
df_pos["resp_time"] = df_pos["resp_time"] / 60000
df_neg["resp_time"] = df_neg["resp_time"] / 60000
df_pos = df_pos.drop_duplicates()
df_neg = df_neg.drop_duplicates()

print(np.var(df_pos["resp_time"]), max(df_pos["resp_time"]), df_pos["resp_time"].mean(), df_pos["resp_time"].median())
print(np.var(df_neg["resp_time"]), max(df_neg["resp_time"]), df_neg["resp_time"].mean(), df_neg["resp_time"].median())

plt.hist(x=df_pos["resp_time"], bins=100, range=(0, 200), color="green", density=True)
plt.hist(x=df_neg["resp_time"], bins=100, range=(0, 200), color="red", density=True)
plt.savefig("Pos_test.png", bbox_inches="tight")

t = stats.ttest_ind(a=df_pos["resp_time"], b=df_neg["resp_time"], equal_var=False, alternative="less")

print(t)

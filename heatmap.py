import pandas as pd
import os
from sqlalchemy import create_engine
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

engine = create_engine(os.environ["DB_STRING"])

query = """
SELECT C.conv_id, C.inter_nr, C.msg_nr, C.tweet_id, C.user_id, C.timestamp, C.DiffTimeStamp resp_time, C.sentiment_change
FROM Conversations_2 C
WHERE C.airline = "KLM" 
AND (C.conv_id, C.timestamp) IN
    (
    SELECT C.conv_id, MIN(C.timestamp)
    FROM Conversations_2 C
    GROUP BY C.conv_id
    )
AND (C.conv_id, 56377143) IN
    (
    SELECT C.conv_id, C.user_id
    FROM Conversations C
    )
"""


df_hm = pd.read_sql_query(query, engine)
for i in range(len(df_hm)):
    df_hm.loc[i, "month"] = datetime.fromtimestamp(df_hm.loc[i, "timestamp"] / 1000).strftime('%m')
    df_hm.loc[i, "day"] = datetime.fromtimestamp(df_hm.loc[i, "timestamp"] / 1000).strftime('%d')

df_hm = df_hm.set_index(["conv_id", "inter_nr", "msg_nr"]).sort_index()
df_hm.to_sql("HeatmapData", engine, schema="Tweets_Data", if_exists="replace")


df_hm = pd.read_sql_table("HeatmapData", engine)
df_hm.loc[len(df_hm)] = [0, 0, 0, 0, 0, 0, 0, 0, "04", "01"]



hmdata = df_hm.groupby(["Month", "Day"])["sentiment_change"].mean().dropna().to_frame(name='total_sentiment').reset_index()
hmdata = hmdata.reset_index().pivot(columns='Month', index='Day', values='total_sentiment')
hmdata["04"]["01"] = np.NaN

fig = plt.figure(figsize=(16, 9))
color = sns.color_palette("coolwarm_r", as_cmap=True)
sns.heatmap(data=hmdata, vmin=-0.5, vmax=0.5, xticklabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                                                                "Sep", "Oct", "Nov", "Dec"], annot=True,cmap=color)
plt.title("Average sentiment change per day (KLM)", {'fontsize': 16,'fontweight' : "bold"})

plt.savefig("heatmap_2.png", bbox_inches='tight')



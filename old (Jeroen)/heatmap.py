import pandas as pd
import os
from sqlalchemy import create_engine
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

engine = create_engine(os.environ["DB_STRING"])

query = """
SELECT C.conv_id, C.inter_nr, C.msg_nr, C.tweet_id, C.user_id, C.timestamp, C.sentiment_change
FROM Conversations C
WHERE C.airline = "KLM" 
AND (C.conv_id, C.timestamp) IN
    (
    SELECT C.conv_id, MIN(C.timestamp)
    FROM Conversations C
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

hmdata = df_hm.groupby(["month", "day"])["sentiment_change"].sum().dropna().to_frame(name='total_sentiment').reset_index()
hmdata = hmdata.reset_index().pivot(columns='month', index='day', values='total_sentiment')
fig = plt.figure(figsize=(16, 9))
color = sns.color_palette("coolwarm", as_cmap=True)
ax = sns.heatmap(data=hmdata, vmin=-20, vmax=20, annot=True, cmap=color)

plt.savefig("heatmap.png", bbox_inches='tight')

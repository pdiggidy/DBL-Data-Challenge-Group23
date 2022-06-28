import pandas as pd
import os
from sqlalchemy import create_engine
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def heatmap(month):
    engine = create_engine(os.environ["DB_STRING"])
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                                 "Sep", "Oct", "Nov", "Dec"]

    month = str(month)  # Making sure the month is a string, and always of length 2 to match the columns
    if len(month) == 1:
        month = f"0{month}"

    query = """
    SELECT C.conv_id, C.inter_nr, C.msg_nr, C.timestamp, C.sentiment_change
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
        df_hm.loc[i, "Month"] = datetime.fromtimestamp(df_hm.loc[i, "timestamp"] / 1000).strftime('%m')
        df_hm.loc[i, "Day"] = datetime.fromtimestamp(df_hm.loc[i, "timestamp"] / 1000).strftime('%d')

    df_hm.loc[len(df_hm)] = [0, 0, 0, 0, 0, "04", "01"]  # This is so April is in the heatmap
    df_hm = df_hm.set_index(["conv_id", "inter_nr", "msg_nr"]).sort_index()
    # df_hm.to_sql("HeatmapData", engine, schema="Tweets_Data", if_exists="replace")  #

    hmdata = df_hm.groupby(["Month", "Day"])["sentiment_change"].mean().dropna().to_frame(name='total_sentiment').reset_index()
    hmdata = hmdata.reset_index().pivot(columns='Month', index='Day', values='total_sentiment')
    hmdata["04"]["01"] = np.NaN

    fig = plt.figure(figsize=(16, 9))
    color = sns.color_palette("coolwarm_r", as_cmap=True)
    if month != "all":
        hmdata = hmdata[month]
        ax = sns.heatmap(data=hmdata[:, np.newaxis], vmin=-0.5, vmax=0.5,
                    xticklabels=[month_list[int(month) - 1]], annot=True, cmap=color)
        ax.tick_params(labelsize=18)
        ax.set_xlabel("Month", size=18)
        ax.set_ylabel("Day", size=18)
        ax.set_yticks([1,5,10,15,20,25,30])
        ax.set_yticklabels([1,5,10,15, 20,25,30])

    if month == "all":
        ax = sns.heatmap(data=hmdata, vmin=-0.5, vmax=0.5,
                    xticklabels=month_list, annot=True, cmap=color)
        ax.tick_params(labelsize=18)
        ax.set_xlabel("Month", size=18)
        ax.set_ylabel("Day", size=18)
        ax.set_yticks([1,5,10,15,20,25,30])
        ax.set_yticklabels([1,5,10,15, 20,25,30])

    ax.collections[0].colorbar.ax.tick_params(labelsize=25)
    plt.title("Average sentiment change per day (KLM)", {'fontsize': 24, 'fontweight': "bold"})
    plt.savefig(f"heatmap_{month}.png", bbox_inches='tight')
    plt.show()




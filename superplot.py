from sqlalchemy import create_engine
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
import seaborn as sns
import re

from datetime import datetime
import statistics as st

connection = create_engine(os.environ["DB_STRING"]).connect()

q = """SELECT company, sentiment, id_str, in_reply_to_status_id_str, user_id_str, timestamp_ms/1000 as cur_timestamp 
    FROM All_tweets 
    WHERE company=0 
    LIMIT 400000"""
all_tweets_df = pd.read_sql(q, connection)
all_tweets_df["is_klm"] = all_tweets_df["user_id_str"] == 56377143

connection.close()

# add timestamp
all_tweets_df["cur_timestamp"] = all_tweets_df["cur_timestamp"].astype("int64")
all_tweets_df["cur_date"] = all_tweets_df["cur_timestamp"].apply(lambda ms: datetime.fromtimestamp(ms))
all_tweets_df["cur_time_in_date"] = all_tweets_df["cur_date"].apply(lambda date: date.replace(year=2000, month=1, day=1))
tweetID_timestamp = all_tweets_df.set_index("id_str")["cur_timestamp"].to_dict()
# replied to something
df_resp = all_tweets_df.dropna(subset="in_reply_to_status_id_str")
df_resp = df_resp.astype({"in_reply_to_status_id_str":"int64"})
# collect previous timestamp
df_resp["prev_timestamp"] = df_resp["in_reply_to_status_id_str"].apply(lambda prev_id: tweetID_timestamp.get(prev_id,None))
df_resp.dropna(subset="prev_timestamp", inplace=True)
df_resp["prev_timestamp"] = df_resp["prev_timestamp"].astype("int64")
# collect previous dates
df_resp["prev_date"] = df_resp["prev_timestamp"].apply(lambda timestamp: datetime.fromtimestamp(timestamp))
df_resp["prev_time_in_date"] = df_resp["prev_date"].apply(lambda date: date.replace(year=2000, month=1, day=1))
# calculate difference in timestamp
df_resp["dif_timestamp"] = df_resp["cur_timestamp"] - df_resp["prev_timestamp"]

# tweets of klm:
klm_df = df_resp[df_resp["is_klm"]]
# sort on time of day
klm_df = klm_df.sort_values("prev_time_in_date")
# calculate moving average
klm_df["dif_timestamp_moving"] = klm_df["dif_timestamp"].rolling(int(16000/24)).median()
klm_df.dropna(subset="dif_timestamp_moving", inplace=True)
# format to time
klm_df["dif_time_moving"] = klm_df["dif_timestamp_moving"].apply(lambda timestamp: datetime(2000,1,1) +
                                                                 (datetime.fromtimestamp(timestamp) -
                                                                  datetime.fromtimestamp(0)))

def plot_response_time():
    figg1, axx1 = plt.subplots()
    figg1.suptitle("Response time over time of day")

    x_prev_timee = klm_df["prev_time_in_date"]
    y_response_timee = klm_df["dif_time_moving"]

    axx1.plot(x_prev_timee, y_response_timee)

    # axx1.xaxis.set_major_locator(HourLocator())
    axx1.xaxis.set_major_formatter(DateFormatter('%H:%M'))

    # axx1.yaxis.set_major_locator(HourLocator())
    axx1.yaxis.set_major_formatter(DateFormatter('%H:%M'))

    axx1.set_xlabel("hour of the day")
    axx1.set_ylabel("response time")

    axx1.set_ylim(datetime(2000, 1, 1), datetime(2000, 1, 1, 0, 30))
    plt.show()


def plot_sent_recieved():
    figg2, axx2 = plt.subplots(figsize=(15, 5))

    x_current_timee = all_tweets_df["cur_time_in_date"]
    y_recievedd = (all_tweets_df["is_klm"] == False).astype(int)
    y_sentt = all_tweets_df["is_klm"].astype(int)

    histogramm = sns.histplot(x=x_current_timee, weights=y_recievedd, label="recieved", bins=24, color="navy", ax=axx2)
    sns.histplot(x=x_current_timee, weights=y_sentt, label="sent", bins=24, color="royalblue", ax=axx2)

    axx2.set_title("Amount of tweets sent and recieved per hour of the day", fontsize=21)
    axx2.set_xlabel("hour of the day", fontsize=11)
    axx2.set_ylabel("amount of tweets sent/recieved", fontsize=11)
    axx2.set_xlim(datetime(2000, 1, 1), datetime(2000, 1, 1, 23, 59, 59, 59))
    axx2.legend()

    axx2.xaxis.set_major_formatter(DateFormatter("%H:%M"))

    # create ratios and print their text
    y_countss = []
    locationss = []
    for barr in histogramm.get_children():
        if isinstance(barr, matplotlib.patches.Rectangle) == False:
            break
        x_locc = barr.get_x() + barr.get_width() / 2.0
        y_locc = barr.get_height()
        y_countss.append(y_locc)
        locationss.append((x_locc, y_locc))
    y_countss = np.array(y_countss)
    y_ratio_inputss = np.round(y_countss[len(y_countss) // 2:] / y_countss[:len(y_countss) // 2], 2)
    locations_inputss = locationss[len(locationss) // 2:]

    for ((x_locc, y_locc), textt) in zip(locations_inputss, y_ratio_inputss):
        axx2.text(x_locc, y_locc, textt, ha='center', va='bottom', color="lightcyan")
    plt.show()

def plot_superplot():
    ### Plot 1: Histogram - Amount of tweets sent and recieved per hour of the day
    fig1, ax1 = plt.subplots(figsize=(15, 5))

    x_current_time = all_tweets_df["cur_time_in_date"]
    y_recieved = (all_tweets_df["is_klm"] == False).astype(int)
    y_sent = all_tweets_df["is_klm"].astype(int)

    sns.histplot(x=x_current_time, weights=y_recieved, label="recieved", bins=24, color="navy", ax=ax1)
    sns.histplot(x=x_current_time, weights=y_sent, label="sent", bins=24, color="royalblue", ax=ax1)

    ax1.set_title("Amount of tweets sent and recieved per hour of the day", fontsize=21)
    ax1.set_xlabel("hour of the day", fontsize=11)
    ax1.set_ylabel("amount of tweets sent/recieved", fontsize=11)
    ax1.set_xlim(datetime(2000, 1, 1), datetime(2000, 1, 1, 23, 59, 59, 59))
    ax1.legend(loc=2)

    # ax1.xaxis.set_major_locator(HourLocator())
    ax1.xaxis.set_major_formatter(DateFormatter("%H:%M"))

    #### Plot 2: Text - Ratio between sent and recieved tweets
    y_counts = []
    locations = []
    for bar in ax1.get_children():
        if isinstance(bar, matplotlib.patches.Rectangle) == False:
            break
        x_loc = bar.get_x() + bar.get_width() / 2.0
        y_loc = bar.get_height()
        y_counts.append(y_loc)
        locations.append((x_loc, y_loc))
    y_counts = np.array(y_counts)
    y_ratio_inputs = np.round(y_counts[len(y_counts) // 2:] / y_counts[:len(y_counts) // 2], 2)
    locations_inputs = locations[len(locations) // 2:]

    for ((x_loc, y_loc), text) in zip(locations_inputs, y_ratio_inputs):
        ax1.text(x_loc, y_loc, text, ha='center', va='bottom', color="lightcyan")

    #### Plot 3: Lineplot - Response time over time of the day
    ax3 = ax1.twinx()

    x_prev_time = klm_df["prev_time_in_date"]
    y_response_time = klm_df["dif_time_moving"]

    ax3.plot(x_prev_time, y_response_time, color="orangered", linewidth=3, label="response time")

    # ax3.xaxis.set_major_locator(HourLocator(interval=2))
    ax3.xaxis.set_major_formatter(DateFormatter('%H:%M'))

    # ax3.yaxis.set_major_locator(matplotlib.dates.MinuteLocator([5,8]))
    ax3.yaxis.set_major_formatter(DateFormatter('%H:%M'))

    ax3.set_xlabel("hour of the day")
    ax3.set_ylabel("response time")
    ax3.legend(loc=1)

    ax3.set_ylim(datetime(2000, 1, 1), datetime(2000, 1, 1, 0, 25))
    plt.show()

plot_response_time()
plot_sent_recieved()
plot_superplot()
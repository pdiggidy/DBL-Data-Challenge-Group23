from sqlalchemy import create_engine
import os

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import seaborn as sns
from datetime import datetime


def month_data_superplot(month, all_tweets_df):
    month = int(month)
    all_tweets_df_copy = all_tweets_df.copy()
    months_series = all_tweets_df_copy.cur_timestamp.apply(lambda s: datetime.fromtimestamp(s).month)
    all_tweets_df_copy[months_series == month]
    df = all_tweets_df[months_series == month].copy().reset_index(drop=True)
    return df

def plot_superplot_heatmap_in_plot(month_number):

    connection = create_engine(os.environ["DB_STRING"]).connect()

    q = """SELECT company, sentiment, id_str, in_reply_to_status_id_str, user_id_str, timestamp_ms/1000 as cur_timestamp 
           FROM All_tweets 
           WHERE company=0 AND lang='en'
           LIMIT 400000"""
    all_tweets_df = pd.read_sql(q, connection)
    looking_for_airline = 56377143
    all_tweets_df["is_klm"] = all_tweets_df["user_id_str"] == looking_for_airline
    all_tweets_df["cur_timestamp"] = all_tweets_df["cur_timestamp"].astype("int64")

    connection.close()

    all_tweets_df = month_data_superplot(month_number, all_tweets_df)
    # add timestamp
    all_tweets_df["cur_date"] = all_tweets_df["cur_timestamp"].apply(lambda ms: datetime.fromtimestamp(ms))
    all_tweets_df["cur_time_in_date"] = all_tweets_df["cur_date"].apply(lambda date: date.replace(year=2000, month=1, day=1))
    all_tweets_df["cur_hour"] = all_tweets_df["cur_time_in_date"].dt.hour
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
    klm_first_cycle = klm_df[["prev_time_in_date", "dif_timestamp"]].set_index("prev_time_in_date").copy()
    add_previous_cycle_df = klm_first_cycle.loc["2000-01-01 23":].copy()
    add_previous_cycle_df.index = add_previous_cycle_df.index.map(lambda x: x.replace(year=1999,month=12,day=31))
    klm_concat = pd.concat([add_previous_cycle_df, klm_first_cycle])
    klm_concat_rolling = klm_concat.rolling("3600s").median()
    klm_df["dif_time_moving"] = klm_concat_rolling.loc["2000"].to_numpy()

    klm_df["dif_time_in_date_moving"] = klm_df["dif_time_moving"].apply(lambda timestamp: datetime(2000,1,1) +
                                                        (datetime.fromtimestamp(timestamp) - datetime.fromtimestamp(0)))

    # create data for heatmap
    connection = create_engine(os.environ["DB_STRING"]).connect()
    q_heat = """SELECT *
           FROM HeatmapData
           """
    heat_data_df = pd.read_sql(q_heat, connection)
    connection.close()

    heat_data_df["hour"] = heat_data_df["timestamp"].apply(lambda timestamp: datetime.fromtimestamp(timestamp/1000).hour)

    pos_neg_df = heat_data_df[["hour", "sentiment_change"]].groupby("hour").mean()
    pos_neg_df.columns = ["total"]

    #####heatmap in other plots#################################################################################
    ### Plot 1: Histogram - Amount of tweets sent and recieved per hour of the day
    fig1, (ax1, ax10) = plt.subplots(2, 1, figsize=(13, 6), gridspec_kw={"height_ratios": (60, 1)})

    x_current_time = all_tweets_df["cur_time_in_date"]
    y_recieved = (all_tweets_df["is_klm"] == False).astype(int)
    y_sent = all_tweets_df["is_klm"].astype(int)

    sns.histplot(x=x_current_time, weights=y_recieved, label="Recieved", bins=24, color="navy", ax=ax1)
    sns.histplot(x=x_current_time, weights=y_sent, label="Sent", bins=24, color="cornflowerblue", shrink=0.7, ax=ax1)

    ax1.set_xlabel("Time (hour of the day)")
    ax1.set_ylabel("Amount of tweets")
    ax1.set_xlim(datetime(2000, 1, 1), datetime(2000, 1, 1, 23, 59, 59, 59))

    ax1.xaxis.set_major_formatter(DateFormatter("%H:%M"))

    ###########################################################################################################
    #### Text for plot 1 - Ratio between sent and recieved tweets
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
    y_ratio_inputs = np.round(y_counts[len(y_counts) // 2:] / y_counts[:len(y_counts) // 2] * 100, 0).astype(int)
    locations_inputs = locations[len(locations) // 2:]

    for ((x_loc, y_loc), text) in zip(locations_inputs, y_ratio_inputs):
        ax1.text(x_loc, y_loc, f"{text}%", ha='center', va='bottom', color="lightcyan", fontsize=11)

    ###########################################################################################################
    #### Plot 2: Lineplot - Response time over time of the day
    ax2 = ax1.twinx()

    x_prev_time = klm_df["prev_time_in_date"]
    y_response_time = klm_df["dif_time_in_date_moving"]

    ax2.plot(x_prev_time, y_response_time, color="orangered", linewidth=3, label="Response time")

    ax2.set_xlabel("Time (hour of the day)")
    ax2.set_ylabel("Response time (hours)")
    ax2.set_ylim(datetime(2000, 1, 1), datetime(2000, 1, 1, 0, 25))

    ax2.yaxis.set_major_formatter(DateFormatter('%H:%M'))

    ###########################################################################################################
    ### heatmap
    pos_neg_df_copy = pos_neg_df.sort_values("total").copy()
    pos_neg_df_copy.iloc[0, 0] = pos_neg_df_copy.iloc[1, 0]
    pos_neg_df_copy.sort_index(inplace=True)

    range_colormap = np.linspace(0, 0.55, 101)
    map_red = [(0.7 + (3 * i / 8.5), i, i) for i in range_colormap]
    map_red.reverse()
    cmap = [(i / 10, 0, 0) for i in range(5, 10)] + [(1, i / 10, i / 10) for i in range(9)]

    sns.heatmap(pos_neg_df_copy[["total"]].transpose(), ax=ax10, cbar=False, cmap=cmap, xticklabels=False, robust=True)
    ax10.set_xlabel("")
    ax10.set_ylabel("")

    color_pos = ax10.get_position()
    hist_pos = ax1.get_position()
    ax10.set_position([hist_pos.x0, hist_pos.y0, color_pos.width, color_pos.height])

    ### set fontsizes
    ax1.set_title("Response time compared to ratio\n of sent and received tweets of KLM (fig 5)",
                  fontsize=24, y=1.03, weight="bold")

    ax1.xaxis.label.set_fontsize(18)
    ax1.yaxis.label.set_fontsize(18)
    ax2.yaxis.label.set_fontsize(18)

    ax1.tick_params(labelsize=16)
    ax2.tick_params(labelsize=16)

    ax1.legend(loc=2, handles=ax1.get_legend_handles_labels()[0] + ax2.get_legend_handles_labels()[0],
               fontsize=16, bbox_to_anchor=(0.07, 1))
    plt.savefig("superplot.png", bbox_inches="tight")
    plt.show()

# plot_superplot_heatmap_in_plot(1)


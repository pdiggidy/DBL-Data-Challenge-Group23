from sqlalchemy import create_engine
import os

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import seaborn as sns
from datetime import datetime

connection = create_engine(os.environ["DB_STRING"]).connect()

q = """SELECT company, sentiment, id_str, in_reply_to_status_id_str, user_id_str, timestamp_ms/1000 as cur_timestamp 
       FROM All_tweets 
       WHERE company=0 AND lang='en'
       LIMIT 400000"""
all_tweets_df = pd.read_sql(q, connection)
looking_for_airline = 56377143
all_tweets_df["is_klm"] = all_tweets_df["user_id_str"] == looking_for_airline

connection.close()

# add timestamp
all_tweets_df["cur_timestamp"] = all_tweets_df["cur_timestamp"].astype("int64")
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
pos_neg_df = pd.DataFrame()
tweets_not_klm_df = all_tweets_df[all_tweets_df["is_klm"] == False]
klm_pos = tweets_not_klm_df[tweets_not_klm_df["sentiment"] == "pos"][["cur_hour", "sentiment"]]
klm_neu = tweets_not_klm_df[tweets_not_klm_df["sentiment"] == "neu"][["cur_hour", "sentiment"]]
klm_neg = tweets_not_klm_df[tweets_not_klm_df["sentiment"] == "neg"][["cur_hour", "sentiment"]]

total = tweets_not_klm_df[["cur_hour", "sentiment"]].groupby("cur_hour").count()
pos_neg_df["klm_pos"] = klm_pos.groupby("cur_hour").count() / total
pos_neg_df["klm_neu"] = klm_neu.groupby("cur_hour").count() / total
pos_neg_df["klm_neg"] = klm_neg.groupby("cur_hour").count() / total
pos_neg_df["total"] = 1 * pos_neg_df["klm_pos"] + 0 * pos_neg_df["klm_neu"] + -1 * pos_neg_df["klm_neg"]


def plot_response_time():
    figg1, axx1 = plt.subplots()
    figg1.suptitle("Response time over time of day")

    x_prev_timee = klm_df["prev_time_in_date"]
    y_response_timee = klm_df["dif_time_in_date_moving"]

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


def plot_heatmap():
    cmap = [(i / 10, 0, 0) for i in range(5, 10)] + [(1, i / 10, i / 10) for i in range(9)]
    figg2, axx2 = plt.subplots(figsize=(12, 1))
    sns.heatmap(pos_neg_df[["total"]].transpose(), ax=axx2, cmap=cmap)
    plt.show()


def plot_superplot_heatmap_in_plot():
    #####heatmap in other plots#################################################################################
    ### Plot 1: Histogram - Amount of tweets sent and recieved per hour of the day
    fig1, (ax1, ax10) = plt.subplots(2, 1, figsize=(15, 6), gridspec_kw={"height_ratios": (60, 1)})

    x_current_time = all_tweets_df["cur_time_in_date"]
    y_recieved = (all_tweets_df["is_klm"] == False).astype(int)
    y_sent = all_tweets_df["is_klm"].astype(int)

    sns.histplot(x=x_current_time, weights=y_recieved, label="recieved", bins=24, color="navy", ax=ax1)
    sns.histplot(x=x_current_time, weights=y_sent, label="sent", bins=24, color="cornflowerblue", shrink=0.7, ax=ax1)

    ax1.set_xlabel("time (hour of the day)")
    ax1.set_ylabel("tweets sent/recieved (freq)")
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

    ax2.plot(x_prev_time, y_response_time, color="orangered", linewidth=3, label="response time")

    ax2.set_xlabel("time (hour of the day)")
    ax2.set_ylabel("response time (hours)")
    ax2.set_ylim(datetime(2000, 1, 1), datetime(2000, 1, 1, 0, 25))

    ax2.yaxis.set_major_formatter(DateFormatter('%H:%M'))

    ###########################################################################################################
    ### heatmap
    cmap = [(i / 10, 0, 0) for i in range(5, 10)] + [(1, i / 10, i / 10) for i in range(9)]

    sns.heatmap(pos_neg_df[["total"]].transpose(), ax=ax10, cbar=False, cmap=cmap, xticklabels=False, robust=True)
    ax10.set_xlabel("")
    ax10.set_ylabel("")

    color_pos = ax10.get_position()
    hist_pos = ax1.get_position()
    ax10.set_position([hist_pos.x0, hist_pos.y0, color_pos.width, color_pos.height])

    ### set fontsizes
    ax1.set_title("Response time compared to ratio sent and recieved tweets", fontsize=25)

    ax1.xaxis.label.set_fontsize(16)
    ax1.yaxis.label.set_fontsize(16)
    ax2.yaxis.label.set_fontsize(16)

    ax1.tick_params(labelsize=14)
    ax2.tick_params(labelsize=14)

    ax1.legend(handles=ax1.get_legend_handles_labels()[0] + ax2.get_legend_handles_labels()[0],
               fontsize=14, bbox_to_anchor=(0.27, 1.01))

    plt.show()


def plot_superplot_heatmap_in_hist():
    ###Colored bars################################################################################################
    ### Plot 1: Histogram - Amount of tweets sent and recieved per hour of the day
    fig1, ax1 = plt.subplots(figsize=(15, 6))

    x_current_time = all_tweets_df["cur_time_in_date"]
    y_recieved = (all_tweets_df["is_klm"] == False).astype(int)
    y_sent = all_tweets_df["is_klm"].astype(int)

    sns.histplot(x=x_current_time, weights=y_recieved, label="recieved", bins=24, color="navy", linewidth=1.2, ax=ax1)
    sns.histplot(x=x_current_time, weights=y_sent, label="sent", bins=24, color="cornflowerblue", shrink=0.7, ax=ax1)

    ax1.set_xlabel("time (hour of the day)")
    ax1.set_ylabel("tweets sent/recieved (freq)")
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
        ax1.text(x_loc, y_loc, f"{text}%", ha='center', va='bottom', color=(0.2, 0, .4), fontsize=11)

    ###########################################################################################################
    #### Plot 2: Lineplot - Response time over time of the day
    ax2 = ax1.twinx()

    x_prev_time = klm_df["prev_time_in_date"]
    y_response_time = klm_df["dif_time_in_date_moving"]

    ax2.plot(x_prev_time, y_response_time, color="teal", linewidth=3, label="response time")

    ax2.set_xlabel("time (hour of the day)")
    ax2.set_ylabel("response time (hours)")
    ax2.set_ylim(datetime(2000, 1, 1), datetime(2000, 1, 1, 0, 25))

    ax2.yaxis.set_major_formatter(DateFormatter('%H:%M'))

    ###########################################################################################################
    #### set bar colors
    range_pos_neg = max(pos_neg_df["total"]) - min(pos_neg_df["total"])
    range_new = 100
    pos_neg_ratio_df = (pos_neg_df["total"] - min(pos_neg_df["total"])) * (range_new / range_pos_neg)

    range_colormap = np.linspace(0, 0.85, 101)
    sent_color_values = np.array(pos_neg_ratio_df, dtype=int)
    map_red = [(0.7 + (3 * i / 8.5), i, i) for i in range_colormap]

    children = ax1.get_children()
    for bar_i in range(24):
        bar1 = children[bar_i]
        bar2 = children[bar_i + 24]
        bar1.set_facecolor(map_red[sent_color_values[bar_i]])
        bar2.set_facecolor((.9, 0.4, .25))

    ### set fontsizes
    ax1.set_title("Response time compared to ratio sent and recieved tweets", fontsize=25)

    ax1.xaxis.label.set_fontsize(16)
    ax1.yaxis.label.set_fontsize(16)
    ax2.yaxis.label.set_fontsize(16)

    ax1.tick_params(labelsize=14)
    ax2.tick_params(labelsize=14)

    ax1.legend(handles=ax1.get_legend_handles_labels()[0] + ax2.get_legend_handles_labels()[0],
               fontsize=14, bbox_to_anchor=(0.27, 1.01))

    plt.show()

plot_response_time()
plot_sent_recieved()
plot_heatmap()
plot_superplot_heatmap_in_plot()
plot_superplot_heatmap_in_hist()

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import swifter


def change(row):
    start = row["start"]
    end = row["end"]

    if start == "pos":
        if end == "neg":
            return -1
        if end == "neu":
            return 0
        else:
            return 1

    elif start == "neu":
        if end == "neu":
            return 0
        elif end == "pos":
            return 1
        else:
            return -1
    elif start == "neg":
        if end == "neg":
            return 0
        else:
            return 1

def box_plots(month):

    engine = create_engine(os.environ["DB_STRING"])

    query = """SELECT All_tweets.sentiment as "end"
        FROM Conversations_max_15_updated Conversations
        INNER JOIN All_tweets on Conversations.tweet_id = All_tweets.id_str
        WHERE (Conversations.conv_id, Conversations.msg_nr) in
            (SELECT Conversations.conv_id, max(Conversations.msg_nr)
            FROM Conversations_max_15_updated Conversations group by Conversations.conv_id)
        AND All_tweets.lang = "en"
    """

    df_ends = pd.read_sql(query, engine)

    query_start = query = """SELECT All_tweets.sentiment as "start", company, timestamp_ms 
        FROM Conversations_max_15_updated Conversations
        INNER JOIN All_tweets on Conversations.tweet_id = All_tweets.id_str
        WHERE (Conversations.conv_id, Conversations.msg_nr) in
            (SELECT Conversations.conv_id, min(Conversations.msg_nr)
            FROM Conversations_max_15_updated Conversations group by Conversations.conv_id)
        AND All_tweets.lang = "en"
    """
    df_starts = pd.read_sql(query_start, engine)

    df_all = pd.concat([df_starts, df_ends], axis=1)
    df_all.dropna(inplace=True)
    df_all["month"] = df_all.timestamp_ms.apply(lambda s: datetime.fromtimestamp(s/1000).month)
    if month != "all":
        df = df_all[df_all["month"] == int(month)]

    df_all["change"] = df_all.swifter.apply(change, axis=1)
    df = df_all


    df = df.groupby("company")

    changes_dict = {}
    pos = []
    neu = []
    neg = []
    for name, group in df:
        vals = group["change"].value_counts(normalize=True)
        ls = []
        for row in vals:
            ls.append(row)
        changes_dict[name] = ls
        pos.append(changes_dict[name][0])
        neu.append(changes_dict[name][1])
        neg.append(changes_dict[name][2])

    # British Airways, Air France, EasyJet, Lufthansa, Ryanair, VirginAtlantic
    names_with = ["British Airways", "Air France", "EasyJet", "Lufthansa", "Ryanair", "VirginAtlantic"]
    names_without = ["KLM", "AmericanAir", "AirBerlin", "SingaporeAir", "Qantas", "Etihad"]
    with_numbers = [2, 1, 6, 4, 7, 11]
    without_numbers = [0, 3, 5, 8, 9, 10]

    pos_with = [pos[i] for i in with_numbers]
    pos_without = [pos[i] for i in without_numbers]
    neu_with = [neu[i] for i in with_numbers]
    neu_without = [neu[i] for i in without_numbers]
    neg_with = [neg[i] for i in with_numbers]
    neg_without = [neg[i] for i in without_numbers]

    ### Box Plots

    box = pd.DataFrame({"pos_with": np.multiply(pos_with, 100), "pos_without": np.multiply(pos_without, 100),
                        "neu_with": np.multiply(neu_with, 100), "neu_without": np.multiply(neu_without, 100),
                        "neg_with": np.multiply(neg_with, 100), "neg_without": np.multiply(neg_without, 100)})

    fig3, ax3 = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(10, 7))
    ax3[0].boxplot(box[["pos_with", "pos_without"]], patch_artist=True, boxprops=dict(facecolor=(0.2, 0.7, 0.2)),
                   medianprops=dict(color=(0.2, 0.4, 0.9), linewidth=2), widths=(0.5, 0.5))
    ax3[1].boxplot(box[["neg_with", "neg_without"]], patch_artist=True, boxprops=dict(facecolor="orange"),
                   medianprops=dict(color=(0.2, 0.4, 0.9), linewidth=2), widths=(0.5, 0.5))
    ax3[0].set_xticklabels(["With\nNames", "Without\nNames"], size=16)
    ax3[1].set_xticklabels(["With\nNames", "Without\nNames"], size=16)
    ax3[0].tick_params(labelsize=18)
    ax3[1].tick_params(labelsize=18)
    ax3[0].set_title("Increase", size=20)
    ax3[1].set_title("Decrease", size=20)
    ax3[0].set_ylabel("Percentage", size=18)
    fig3.suptitle("Distribution of Sentiment Change", size=24)
    #ax3[0].text(s="Virgin Atlantic", x=1, y=min(box["pos_with"] + 1), size=12, ha="center")
    #ax3[1].text(s="Virgin Atlantic", x=1, y=max(box["neg_with"] - 2), size=12, ha="center")
    plt.tight_layout()
    plt.show()



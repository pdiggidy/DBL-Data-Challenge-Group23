import pandas as pd
import os
from sqlalchemy import create_engine
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

#df = pd.read_pickle("changes")
#names = ["KLM", "AirFrance", "BritishAirways", "AmericanAir", "Lufthansa", "AirBerlin",
#                 "EasyJet", "Ryanair", "SingaporeAir", "Qantas", "Etihad", "VirginAtlantic"]

def Boxplot(month):
    engine = create_engine(os.environ["DB_STRING"])
    names_with = ["BritishAirways", "AirFrance", "EasyJet", "Lufthansa", "Ryanair", "VirginAtlantic"]
    names_without = ["KLM", "AmericanAir", "SingaporeAir", "Qantas"]

    pos_with = list()
    halfpos_with = list()
    neu_with = list()
    halfneg_with = list()
    neg_with = list()
    pos_without = list()
    halfpos_without = list()
    neu_without = list()
    halfneg_without = list()
    neg_without = list()


    for airline in names_with:
        query = f"""
           SELECT C.conv_id, C.inter_nr, C.airline, C.sentiment_change
           FROM Conversations_2 C
           WHERE C.airline = "{airline}"
        """

        df = pd.read_sql_query(query, engine)
        df = df.drop_duplicates()

        pos_with.append(len(df[df["sentiment_change"] == 1]["sentiment_change"]) / len(df["sentiment_change"]))
        halfpos_with.append(len(df[df["sentiment_change"] == 0.5]["sentiment_change"]) / len(df["sentiment_change"]))
        neu_with.append((df[df["sentiment_change"] == 0]["sentiment_change"]) / len(df["sentiment_change"]))
        halfneg_with.append(len(df[df["sentiment_change"] == -0.5]["sentiment_change"]) / len(df["sentiment_change"]))
        neg_with.append(len(df[df["sentiment_change"] == -1]["sentiment_change"]) / len(df["sentiment_change"]))

    for airline in names_without:
        query = f"""
           SELECT C.conv_id, C.inter_nr, C.airline, C.sentiment_change
           FROM Conversations_2 C
           WHERE C.airline = "{airline}"
        """
        df = pd.read_sql_query(query, engine)
        df = df.drop_duplicates()
        pos_without.append(len(df[df["sentiment_change"] == 1]["sentiment_change"]) / len(df["sentiment_change"]))
        halfpos_without.append(len(df[df["sentiment_change"] == 0.5]["sentiment_change"]) / len(df["sentiment_change"]))
        neu_without.append((df[df["sentiment_change"] == 0]["sentiment_change"]) / len(df["sentiment_change"]))
        halfneg_without.append(len(df[df["sentiment_change"] == -0.5]["sentiment_change"]) / len(df["sentiment_change"]))
        neg_without.append(len(df[df["sentiment_change"] == -1]["sentiment_change"]) / len(df["sentiment_change"]))

    box = pd.DataFrame({"pos_with": np.multiply(pos_with,100), "pos_without": np.multiply(pos_without,100),
                        "halfpos_with": np.multiply(halfpos_with,100), "pos_without": np.multiply(pos_without,100),
                        "neu_with": np.multiply(neu_with,100), "neu_without": np.multiply(neu_without,100),
                        "neg_with": np.multiply(halfneg_with, 100), "neg_without": np.multiply(neg_without, 100),
                        "neg_with": np.multiply(neg_with,100), "neg_without": np.multiply(neg_without,100)})

    fig3, ax3 = plt.subplots(nrows=1, ncols=2, sharey=True,figsize=(10,7))
    ax3[0].boxplot(box[["pos_with", "pos_without"]], patch_artist=True,boxprops=dict(facecolor=(0.2, 0.7, 0.2)),
                   medianprops=dict(color=(0.2,0.4,0.9), linewidth=2), widths=(0.5,0.5))
    ax3[1].boxplot(box[["neg_with", "neg_without"]], patch_artist=True, boxprops=dict(facecolor="orange"),
                   medianprops=dict(color=(0.2,0.4,0.9), linewidth=2),widths=(0.5,0.5))
    ax3[0].set_xticklabels(["With\nNames", "Without\nNames"], size=20)
    ax3[1].set_xticklabels(["With\nNames", "Without\nNames"], size=20)
    ax3[0].tick_params(labelsize=18)
    ax3[1].tick_params(labelsize=18)
    ax3[0].set_title("Increase", size=20)
    ax3[1].set_title("Decrease", size=20)
    ax3[0].set_ylabel("Percentage", size=20)
    fig3.suptitle("Distribution of Sentiment Change", size=24)
    ax3[0].text( s="Virgin Atlantic",x=1, y=min(box["pos_with"]+1), size=12, ha="center")
    ax3[1].text( s="Virgin Atlantic",x=1, y=max(box["neg_with"]-2), size=12, ha="center")
    plt.tight_layout()
    plt.show()

Boxplot(1)


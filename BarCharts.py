import os
from sqlalchemy import create_engine
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
import math as math
import statistics
import seaborn as sns
import numpy as np


def BarChart(month: int):
    connection = create_engine(os.environ["DB_STRING"])
    query_max = """
    SELECT C.conv_id, C.sentiment sentiment_last
    FROM Conversations_2 C
    WHERE (C.conv_id, C.msg_nr) in 
          (SELECT C.conv_id, MAX(C.msg_nr)
            FROM Conversations_2 C 
            WHERE C.user_id NOT IN (56377143, 106062176, 18332190, 22536055, 124476322, 
                 38676903, 1542862735, 253340062, 218730857, 45621423, 20626359)
            GROUP BY C.conv_id
                )    
                
    """

    query_min = """
        SELECT C.conv_id, C.sentiment sentiment_first, C.timestamp
        FROM Conversations_2 C
        WHERE (C.conv_id, C.msg_nr) in 
              (SELECT C.conv_id, MIN(C.msg_nr)
                FROM Conversations_2 C 
                WHERE C.user_id NOT IN (56377143, 106062176, 18332190, 22536055, 124476322, 
                     38676903, 1542862735, 253340062, 218730857, 45621423, 20626359)
                GROUP BY C.conv_id
                    )    """
    query_al = """
            SELECT C.conv_id, C.user_id Airline
            FROM Conversations_2 C
            WHERE C.user_id in 
                (56377143, 106062176, 18332190, 22536055, 124476322, 
                 38676903, 1542862735, 253340062, 218730857, 45621423, 20626359)"""

    df_first = pd.read_sql_query(query_min, connection)
    df_last = pd.read_sql_query(query_max, connection)
    df_al = pd.read_sql_query(query_al, connection).drop_duplicates()

    df_t = pd.merge(left=df_first, right=df_last, how="inner", left_on="conv_id", right_on="conv_id")
    df = pd.merge(left=df_t, right=df_al, how="inner",  left_on="conv_id", right_on="conv_id")

    df["month"] = df["timestamp"].apply(lambda s: datetime.fromtimestamp(s/1000).month)
    if month != "all":
        df = df[df["month"] == month]

    df_klm = df[df["Airline"] == 56377143]
    df_ba = df[df["Airline"] == 18332190]
    df_ra = df[df["Airline"] == 1542862735]
    df_ej = df[df["Airline"] == 38676903]

    klm_dic = dict()
    ba_dic = dict()
    ra_dic = dict()
    ej_dic = dict()

    klm_dic["sentiment_first"] = (len(df_klm[df_klm["sentiment_first"] == "neg"]),
                                  len(df_klm[df_klm["sentiment_first"] == "neu"]),
                                  len(df_klm[df_klm["sentiment_first"] == "pos"]))
    klm_dic["sentiment_last"] = (len(df_klm[df_klm["sentiment_last"] == "neg"]),
                                 len(df_klm[df_klm["sentiment_last"] == "neu"]),
                                 len(df_klm[df_klm["sentiment_last"] == "pos"]))
    print(f"klm: {klm_dic}")

    ba_dic["sentiment_first"] = (len(df_ba[df_ba["sentiment_first"] == "neg"]),
                                 len(df_ba[df_ba["sentiment_first"] == "neu"]),
                                 len(df_ba[df_ba["sentiment_first"] == "pos"]))
    ba_dic["sentiment_last"] = (len(df_ba[df_ba["sentiment_last"] == "neg"]),
                                len(df_ba[df_ba["sentiment_last"] == "neu"]),
                                len(df_ba[df_ba["sentiment_last"] == "pos"]))
    print(f"ba: {ba_dic}")

    ra_dic["sentiment_first"] = (len(df_ra[df_ra["sentiment_first"] == "neg"]),
                                 len(df_ra[df_ra["sentiment_first"] == "neu"]),
                                 len(df_ra[df_ra["sentiment_first"] == "pos"]))
    ra_dic["sentiment_last"] = (len(df_ra[df_ra["sentiment_last"] == "neg"]),
                                len(df_ra[df_ra["sentiment_last"] == "neu"]),
                                len(df_ra[df_ra["sentiment_last"] == "pos"]))
    print(f"ra: {ra_dic}")

    ej_dic["sentiment_first"] = (len(df_ej[df_ej["sentiment_first"] == "neg"]),
                                 len(df_ej[df_ej["sentiment_first"] == "neu"]),
                                 len(df_ej[df_ej["sentiment_first"] == "pos"]))
    ej_dic["sentiment_last"] = (len(df_ej[df_ej["sentiment_last"] == "neg"]),
                                len(df_ej[df_ej["sentiment_last"] == "neu"]),
                                len(df_ej[df_ej["sentiment_last"] == "pos"]))
    print(f"ej: {ej_dic}")

    x_axis = np.arange(7)

    plt.bar([x_axis[0], x_axis[4]], [klm_dic["sentiment_first"][0], klm_dic["sentiment_last"][0]],
            alpha=0.5, color="red")
    plt.bar([x_axis[1], x_axis[5]], [klm_dic["sentiment_first"][1], klm_dic["sentiment_last"][1]],
            alpha=0.5, color="orange")
    plt.bar([x_axis[2], x_axis[6]], [klm_dic["sentiment_first"][2], klm_dic["sentiment_last"][2]],
            alpha=0.5, color="green")
    plt.suptitle("KLM", size=22)
    plt.xlabel("Start                          End", size=18)
    plt.xticks([x_axis[0], x_axis[1], x_axis[2], x_axis[4], x_axis[5], x_axis[6]],
               ["neg", "neu", "pos", "neg", "neu", "pos"], size=16)
    plt.yticks(size=16)
    plt.ylabel("Amount of tweets", size=18)
    plt.savefig(f"BarChart_KLM_{month}.png", bbox_inches="tight")
    plt.show()
    plt.clf()

    plt.bar([x_axis[0], x_axis[4]], [ba_dic["sentiment_first"][0], ba_dic["sentiment_last"][0]],
            alpha=0.5, color="red")
    plt.bar([x_axis[1], x_axis[5]], [ba_dic["sentiment_first"][1], ba_dic["sentiment_last"][1]],
            alpha=0.5, color="orange")
    plt.bar([x_axis[2], x_axis[6]], [ba_dic["sentiment_first"][2], ba_dic["sentiment_last"][2]],
            alpha=0.5, color="green")
    plt.suptitle("BritishAirways", size=22)
    plt.xlabel("Start                          End", size=18)
    plt.xticks([x_axis[0], x_axis[1], x_axis[2], x_axis[4], x_axis[5], x_axis[6]],
               ["neg", "neu", "pos", "neg", "neu", "pos"], size=16)
    plt.yticks(size=16)
    plt.ylabel("Amount of tweets", size=18)
    plt.savefig(f"BarChart_BA_{month}.png", bbox_inches="tight")
    plt.show()
    plt.clf()

    plt.bar([x_axis[0], x_axis[4]], [ra_dic["sentiment_first"][0], ra_dic["sentiment_last"][0]],
            alpha=0.5, color="red")
    plt.bar([x_axis[1], x_axis[5]], [ra_dic["sentiment_first"][1], ra_dic["sentiment_last"][1]],
            alpha=0.5, color="orange")
    plt.bar([x_axis[2], x_axis[6]], [ra_dic["sentiment_first"][2], ra_dic["sentiment_last"][2]],
            alpha=0.5, color="green")

    plt.suptitle("RyanAir", size=22)
    plt.xlabel("Start                          End", size=18)
    plt.xticks([x_axis[0], x_axis[1], x_axis[2], x_axis[4], x_axis[5], x_axis[6]],
               ["neg", "neu", "pos", "neg", "neu", "pos"], size=16)
    plt.yticks(size=16)
    plt.ylabel("Amount of tweets", size=18)
    plt.savefig(f"BarChart_RA_{month}.png", bbox_inches="tight")
    plt.show()
    plt.clf()

    plt.bar([x_axis[0], x_axis[4]], [ej_dic["sentiment_first"][0], ej_dic["sentiment_last"][0]],
            alpha=0.5, color="red")
    plt.bar([x_axis[1], x_axis[5]], [ej_dic["sentiment_first"][1], ej_dic["sentiment_last"][1]],
            alpha=0.5, color="orange")
    plt.bar([x_axis[2], x_axis[6]], [ej_dic["sentiment_first"][2], ej_dic["sentiment_last"][2]],
            alpha=0.5, color="green")
    plt.suptitle("EasyJet", size=22)
    plt.xlabel("Start                          End", size=18)

    plt.xticks([x_axis[0], x_axis[1], x_axis[2], x_axis[4], x_axis[5], x_axis[6]],
               ["neg", "neu", "pos", "neg", "neu", "pos"], size=16)
    plt.yticks(size=16)
    plt.ylabel("Amount of tweets", size=18)
    plt.savefig(f"BarChart_EJ_{month}.png", bbox_inches="tight")
    plt.show()
    plt.show()
   # plt.clf()

BarChart(1)
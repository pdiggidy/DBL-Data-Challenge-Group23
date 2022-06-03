# This file requires a local variable so will likely not work on your machine without adding it

import matplotlib.pyplot as plt
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os
import swifter

engine = create_engine(os.environ["DB_STRING"])

sentiment_df = pd.DataFrame()

company_names = ["KLM", "AirFrance", "BritishAirways", "AmericanAir", "Lufthansa", "AirBerlin",
                 "EasyJet", "Ryanair", "SingaporeAir", "Qantas", "Ethihad", "VirginAtlantic"]
company_id_list = [56377143, 106062176, 18332190, 22536055, 124476322, 26223583, 38676903, 1542862735,
                   253340062, 218730857, 45621423, 20626359]


def check_max(row):
    values = [row["SA_neg"], row["SA_neu"], row["SA_pos"]]
    index = values.index(max(values))
    if index == 0:
        return "neg"
    if index == 1:
        return "neu"
    if index == 2:
        return "pos"


def combine(row):
    return (row["SA_neg"] * -1 + row["SA_pos"] * 1)


for count, value in enumerate(company_names):

    query = f""" SELECT *
    FROM {value}_SA
    WHERE user_id_str != {company_id_list[count]}"""

    df = pd.read_sql(query, engine)
    df["airline"] = value
    df["sentiment"] = df.swifter.apply(combine, axis=1)
    sentiment_df = pd.concat([sentiment_df, df], axis=0)

# sentiment_df.to_pickle("sentiments_all")
# sentiment_df = pd.read_pickle("sentiments_all")
sentiment_df["sentiment"].hist(bins=20)
for name, group in sentiment_df.groupby("airline"):
    ax = group["sentiment"].hist(bins=30)
    ax.set_title(name)
    plt.show()

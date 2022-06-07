import os
from sqlalchemy import create_engine
from CompanySort import *
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from Lists import *
import statistics as stat
import seaborn as sns
import numpy as np

connection = create_engine(os.environ["DB_STRING"]).connect()
df_conv = pd.DataFrame()
for x in range(1, 16):
    print(x)
    q = f"""
    SELECT Con.{x} as tweet_id, AT.user_id_str as user_id, {x} as msg_nr, Con.index as conv_id, AT.sentiment as sentiment
        FROM  Conversations_temp Con
        INNER JOIN All_tweets_labeled AT on Con.{x} = AT.id_str
    
    """

    df_t = pd.read_sql_query(q, connection)
    df_conv = pd.concat([df_conv, df_t], ignore_index=True)

df_conv = df_conv.set_index(["conv_id", "msg_nr"])
df_conv = df_conv.sort_index()
print(df_conv)
# engine = create_engine(os.environ["DB_STRING"])  #Deze 2 regels zouden het op de server moeten zetten
# df_conv.to_sql("Conversations_updated", engine, schema="Tweets_Data", if_exists="replace")
#df_conv_numpy = df_conv.to_numpy()
connection.close()

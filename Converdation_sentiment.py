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
for x in range(1, 5):
    print(x)
    q = f"""
    SELECT Con.{x} as tweet_id, AT.user_id_str as user_id, {x} as msg_nr, Con.index as conv_id
        FROM  Conversations Con
        INNER JOIN All_tweets AT on Con.{x} = AT.id_str
    
    """

    df_t = pd.read_sql_query(q, connection)
    df_conv = pd.concat([df_conv, df_t], ignore_index=True)
df_conv_numpy = df_conv.to_numpy()
print(df_conv)
connection.close()

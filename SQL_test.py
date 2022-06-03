# This file requires a local variable so will likely not work on your machine without adding it


import pandas as pd
from Conversations import conversation_builder
import pymysql
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ["DB_STRING"])

df_tweets = pd.read_pickle(r"C:\Users\yamez\Downloads\full_cleaned_data\all_tweets_df (updated with id_str as index).pickle")
df = df_tweets[~df_tweets.index.duplicated(keep="first")]

# df.index = df.index.map(lambda x: int(x))
# df.in_reply_to_status_id_str = df.in_reply_to_status_id_str.map(lambda x: int(x))
# df.in_reply_to_user_id_str = df.in_reply_to_user_id_str.map(lambda x: int(x))
# df.user_id_str = df.user_id_str.map(lambda x: int(x))

conversations_df = conversation_builder(df)

conversations_df.fillna(0, inplace=True)
conversations_df = conversations_df.applymap(lambda x: int(x))
conversations_df.set_index(1, inplace=True)
conversations_df.columns = conversations_df.columns.astype("str")

# conversations_df.to_sql('Conversations', con=engine, if_exists="append", schema="Tweets_Data")
print("done")
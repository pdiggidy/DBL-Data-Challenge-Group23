# This file requires a local variable so will likely not work on your machine without adding it


import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os

df_klm = pd.read_pickle(#######)
engine = create_engine(os.environ["DB_STRING"])

df_klm.index = df_klm.index.map(lambda x:int(x))
df_klm.place = df_klm.place.map(lambda x:f"{x}")
df_klm.hashtags = df_klm.hashtags.map(lambda x:f"{x}")
df_klm.user_mentions = df_klm.user_mentions.map(lambda x:f"{x}")


schema_tweets = '''`KLM` (
`id_str` INT(19) NOT NULL,
`text` LONGTEXT NOT NULL,
`in_reply_to_status_id_str` INT,    
`in_reply_to_user_id_str` INT,
`place` TEXT,
`quote_count` INT,
`reply_count` INT,
`retweet_count` INT,
`favorite_count` INT,
`lang` TEXT,
`timestamp_ms` BIGINT,
`hashtags` TEXT,
`user_mentions` TEXT,
`user_id_str` TEXT,
`company` INT,
`quoted_status_id_str` TEXT,
`latitude` TEXT,
`longitude` TEXT,
UNIQUE KEY `id` (`id_str`) USING HASH,
PRIMARY KEY (`id_str`)'''
#df_klm.to_sql('KLM', con=engine, if_exists="append", schema="testing")
print(len(df_klm))
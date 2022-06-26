import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine(os.environ["DB_STRING"])

query = """
SELECT C.conv_id, C.msg_nr, C.inter_nr, C.tweet_id, C.user_id, C.sentiment, AT.timestamp_ms timestamp, AT.airline
FROM Conversations_Newest_SA_incl_airline C
INNER JOIN All_tweets AT on C.tweet_id = AT.id_str"""

query_resp_time = """
SELECT REPLY.id_str tweet_id, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
FROM All_tweets BASIS
INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str"""

query_max = """
SELECT C.conv_id, C.sentiment sentiment_last
FROM Conversations_Newest_SA_incl_airline C
WHERE (C.conv_id, C.msg_nr) in 
      (SELECT C.conv_id, MAX(C.msg_nr)
        FROM Conversations_Newest_SA_incl_airline C 
        WHERE C.user_id NOT IN (56377143, 106062176, 18332190, 22536055, 124476322, 
             38676903, 1542862735, 253340062, 218730857, 45621423, 20626359)
        GROUP BY C.conv_id
            )    """

query_min = """
    SELECT C.conv_id, C.sentiment sentiment_first
    FROM Conversations_Newest_SA_incl_airline C
    WHERE (C.conv_id, C.msg_nr) in 
          (SELECT C.conv_id, MIN(C.msg_nr)
            FROM Conversations_Newest_SA_incl_airline C 
            WHERE C.user_id NOT IN (56377143, 106062176, 18332190, 22536055, 124476322, 
                 38676903, 1542862735, 253340062, 218730857, 45621423, 20626359)
            GROUP BY C.conv_id
                )    """


def sentiment_change(start, end):
    if start != "neg" and end == "neg":
        return -1
    elif start == "neg" and end != "neg":
        return 1
    else:
        return 0


print(1)
df_base = pd.read_sql_query(query, engine)
print(2)
df_resp_time = pd.read_sql_query(query_resp_time, engine)
print(3)
df_first = pd.read_sql_query(query_min, engine)
print(4)
df_last = pd.read_sql_query(query_max, engine)
print(5)
df_sa = pd.merge(left=df_first, right=df_last, how="left", left_on="conv_id", right_on="conv_id")
print(6)
for i in range(len(df_sa)):
    df_sa.loc[i, "sentiment_change"] = sentiment_change(df_sa.loc[i, "sentiment_first"], df_sa.loc[i, "sentiment_last"])
print(7)
df_pre = pd.merge(left=df_base, right=df_resp_time, how="left", left_on="tweet_id", right_on="tweet_id")
print(8)
df = pd.merge(left=df_pre, right=df_sa, how="left", right_on="conv_id", left_on="conv_id")
print(9)
df = df.set_index(["conv_id", "msg_nr"]).sort_index()
print("uploading")

df.to_sql("Conversations", engine, schema="Tweets_Data", if_exists="replace")


from sqlalchemy import create_engine
import os
import pandas as pd
import regex

engine = create_engine(os.environ["DB_STRING"])

# query = """SELECT text
# FROM All_tweets_labeled, Conversations_max_15_updated
# WHERE All_tweets_labeled.id_str = Conversations_max_15_updated.tweet_id AND Conversations_max_15_updated.conv_id = Conversations_max_15_updated.conv_id
# """

query = """SELECT All_tweets.id_str, All_tweets.text, company
    FROM Conversations_max_15_updated Conversations
    INNER JOIN All_tweets_labeled All_tweets on Conversations.tweet_id = All_tweets.id_str
    WHERE (Conversations.conv_id, Conversations.msg_nr) in 
        (SELECT Conversations.conv_id, max(Conversations.msg_nr)
        FROM Conversations_max_15_updated Conversations group by Conversations.conv_id)
"""

#query = """SELECT a.conv_id, tweet_id
#FROM Conversations_max_15_updated as a
#INNER JOIN
#(SELECT conv_id, MAX(msg_nr) as nr
#FROM Conversations_max_15_updated
#GROUP BY conv_id) as b
#ON a.conv_id = b.conv_id AND a.msg_nr = b.nr
#"""
df_ends = pd.read_sql(query, engine)
print()

regex = r'"( DM)"gmi'

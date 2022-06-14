import re

from sqlalchemy import create_engine
import os
import pandas as pd
import regex
import swifter

engine = create_engine(os.environ["DB_STRING"])

#test
query = """SELECT All_tweets.id_str, All_tweets.text, company
    FROM Conversations_max_15_updated Conversations
    INNER JOIN All_tweets_labeled All_tweets on Conversations.tweet_id = All_tweets.id_str
    WHERE (Conversations.conv_id, Conversations.msg_nr) in
        (SELECT Conversations.conv_id, max(Conversations.msg_nr)
        FROM Conversations_max_15_updated Conversations group by Conversations.conv_id)
    AND All_tweets.lang = "en"
"""


df_ends = pd.read_sql(query, engine)

regex = r'( dm)'

df_ends["check"] = df_ends["text"].swifter.apply(lambda x: re.search(regex, x.lower()))


#print("done")


#text = "Hello can you send us a DM?"

print(re.search(regex, text.lower()))
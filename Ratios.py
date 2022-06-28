from sqlalchemy import create_engine
import os
import pandas as pd
import numpy as np
import regex as re
import swifter

engine = create_engine(os.environ["DB_STRING"])

# query = """SELECT text
# FROM BritishAirways_SA
# WHERE user_id_str = 18332190"""
#
# df_ba = pd.read_sql(query, engine)
# # #print(df_ba)
# #
# # df_ba = df_ba.iloc[np.random.choice(df_ba.index, 1000)]
# # print(len(df_ba))
# #df_ba.to_excel("ba_random sample.xlsx")
#
# names = set(pd.read_excel("ba_random sample_labeled.xlsx", usecols=[2],names=["name"])["name"].tolist())
# #print(names)
# re_names = [re.compile(x) for x in names]
#
# def match_names(text):
#    # print(text)
#     if any(re.search(r,text) for r in re_names):
#         return 1
#     else:
#         return 0
#
# df_ba["personal"] = df_ba["text"].swifter.apply(match_names)#, args=([re_names]), axis=1)
# df_ba.to_pickle("matched.pickle")
#
# print(df_ba["personal"].sum()/len(df_ba["personal"]))

#British Airways, Air France, EasyJet, Lufthansa, Ryanair, VirginAtlantic


query = """SELECT All_tweets.sentiment as "end"
    FROM Conversations_max_15_updated Conversations
    INNER JOIN All_tweets on Conversations.tweet_id = All_tweets.id_str
    WHERE (Conversations.conv_id, Conversations.msg_nr) in
        (SELECT Conversations.conv_id, max(Conversations.msg_nr)
        FROM Conversations_max_15_updated Conversations group by Conversations.conv_id)
    AND All_tweets.lang = "en"
"""


df_ends = pd.read_sql(query, engine)

query_start = query = """SELECT All_tweets.sentiment as "start", company, timestamp_ms
    FROM Conversations_max_15_updated Conversations
    INNER JOIN All_tweets on Conversations.tweet_id = All_tweets.id_str
    WHERE (Conversations.conv_id, Conversations.msg_nr) in
        (SELECT Conversations.conv_id, min(Conversations.msg_nr)
        FROM Conversations_max_15_updated Conversations group by Conversations.conv_id)
    AND All_tweets.lang = "en"
"""
df_starts = pd.read_sql(query_start, engine)
#regex = r'( dm)'

#df_ends["check"] = df_ends["text"].swifter.apply(lambda x: re.search(regex, x.lower()))

df_all = pd.concat([df_starts, df_ends], axis=1)

print(len(df_ends))
print(len(df_starts))
print(len(df_all))

df_all.dropna(inplace=True)

def change(row):
    start = row["start"]
    end = row["end"]

    if start == "pos":
        if end == "neg":
            return -1
        if end == "neu":
            return 0
        else:
            return 1

    elif start == "neu":
        if end =="neu":
            return 0
        elif end == "pos":
            return 1
        else:
            return -1
    elif start == "neg":
        if end ==  "neg":
            return 0
        else:
            return 1

df_all["change"] = df_all.swifter.apply(change, axis=1)

df_all.to_pickle("changes")

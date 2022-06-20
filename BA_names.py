import re

from sqlalchemy import create_engine
import os
import pandas as pd
import numpy as np
import regex as re
import swifter

engine = create_engine(os.environ["DB_STRING"])

query = """SELECT text
FROM BritishAirways_SA
WHERE user_id_str = 18332190"""

df_ba = pd.read_sql(query, engine)
# #print(df_ba)
#
# df_ba = df_ba.iloc[np.random.choice(df_ba.index, 1000)]
# print(len(df_ba))
#df_ba.to_excel("ba_random sample.xlsx")

names = set(pd.read_excel("ba_random sample_labeled.xlsx", usecols=[2],names=["name"])["name"].tolist())
#print(names)
re_names = [re.compile(x) for x in names]

def match_names(text):
   # print(text)
    if any(re.search(r,text) for r in re_names):
        return 1
    else:
        return 0

df_ba["personal"] = df_ba["text"].swifter.apply(match_names)#, args=([re_names]), axis=1)
df_ba.to_pickle("matched.pickle")

print(df_ba["personal"].sum()/len(df_ba["personal"]))

#British Airways, Air France, EasyJet, Lufthansa, Ryanair, VirginAtlantic
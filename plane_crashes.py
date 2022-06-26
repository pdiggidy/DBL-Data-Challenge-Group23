import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import datetime
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

# Dates covered by the data set: 22/05/2019 - 30/03/2022
# Plane crashes in this timeframe:
# (after https://en.wikipedia.org/wiki/List_of_accidents_and_incidents_involving_commercial_aircraft#2019)
#
# June 27 – Angara Airlines Flight 200, engine failure, 2 of 4 crew members died
# August 15 – Ural Airlines Flight 178, double bird strike after takeoff, 74 of 223 passengers injured
# October 4 – Ukraine Air Alliance Flight 4050, fuel exhaustion, 5 of 8 died, 3 injured
# October 17 – PenAir Flight 3296, Overshot runway, 2 injured, 1 of which dies
# November 24 – Busy Bee Dornier Do 228, Crashed into adensely populated area, all 19 occupants + 10 people on the ground died
# December 27 – Bek Air Flight 2100, Crashed on takeoff, 13 of 98 died, 65 injured
# January 8 – Ukraine International Airlines Flight 752, Hit by 2 Iranian missiles, all 176 people on board died
# January 14 – Delta Air Lines Flight 89, Dumped fuel over several neighborhoods/schools, 56 injured
# January 27 – Caspian Airlines Flight 6936, Comes to stop on a road, 2 injured
# February 5 – Pegasus Airlines Flight 2193, Went off the runway of takeoff, all 183 on board died

engine = create_engine(os.environ["DB_STRING"])

query_crash = """
SELECT C.tweet_id, C.sentiment_change smc, C.month, C.day
FROM HeatmapData C
WHERE (C.month, C.day) IN
    (
    (06, 27), (08, 15), (10, 04), (10, 17), (11, 24), (12, 27), (01, 08), (01, 14), (01, 27), (02, 05)
    )"""


query_no_crash = """
SELECT C.tweet_id, C.sentiment_change smc, C.resp_time, C.month, C.day
FROM HeatmapData C
WHERE (C.month, C.day) NOT IN
    (
    (06, 27), (08, 15), (10, 04), (10, 17), (11, 24), (12, 27), (01, 08), (01, 14), (01, 27), (02, 05)
    )"""
df_cr = pd.read_sql_query(query_crash, engine)
df_ncr = pd.read_sql_query(query_no_crash, engine)


t = stats.ttest_ind(a=df_cr["smc"], b=df_ncr["smc"], equal_var=False, alternative="two-sided")
print(t)



from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from main import *

# x = [1,2,3,4,5,6,7,8,9]
# y = [1,1,
#      2,2,2,2,2,2,
#      3,3,3,3,3,
#      4,4,4,
#      5,
#      6,6,
#      7,7,7,
#      ]
# y_series = pd.Series(y)
# print(y_series.mean())

####################################################    PLOT 1
# languages, percentages = tweets_per_language(tweets)
# explode = (0, 0.1, 0, 0)
# fig1, ax1 = plt.subplots()
# ax1.pie(percentages, labels=languages, autopct='%6.1f%%', # shows percentages in pie
#         shadow=False, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#
# plt.title("Distribution of languages of tweets")

####################################################    PLOT 2
tweets_per_day = tweets_per_weekday(tweets)
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.bar(week_days, tweets_per_day, color='maroon',
        width=0.4)

plt.xlabel("Courses offered")
plt.ylabel("No. of students enrolled")
plt.title("Students enrolled in different courses")

####################################################    PLOT 3
tweets_per_day = tweets_per_weekday(tweets)
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.bar(week_days, tweets_per_day, color='maroon',
        width=0.4)

plt.xlabel("Courses offered")
plt.ylabel("No. of students enrolled")
plt.title("Students enrolled in different courses")


plt.show()


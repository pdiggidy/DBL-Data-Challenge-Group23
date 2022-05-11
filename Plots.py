from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from main import tweets
from DataStatistics import *

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
# tweets_per_day = tweets_per_weekday(tweets)
# categories = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# plt.bar(categories, tweets_per_day, color='maroon',
#         width=0.4)
#
# plt.xlabel("Courses offered")
# plt.ylabel("No. of students enrolled")
# plt.title("Students enrolled in different courses")

####################################################    PLOT 3
# y1, y2 = tweets_per_airline(tweets)
# x = np.arange(3)
#
# width = 0.40
#
# # plot data in grouped manner of bar type
# plt.bar(x - 0.2, y1, width)
# plt.bar(x + 0.2, y2, width)

####################################################    PLOT 4
# in_business, out_business = tweets_per_hour(tweets)
# sns.boxplot(data=in_business)
# # sns.boxplot(data=out_business)

####################################################    PLOT 5a
# conversation_length_klm,\
# conversation_length_ba,\
# conversation_length_other = average_conversation_length(cleaned_conversations, tweets)

# sns.boxplot(data=conversation_length_other)

####################################################    PLOT 5b  better?
# conversation_length_klm,\
# conversation_length_ba,\
# conversation_length_other = average_conversation_length(cleaned_conversations, tweets)
#
# airlines = ['KLM', 'BA', 'Other']
# average_lengths = [conversation_length_klm, conversation_length_ba, conversation_length_other]
# plt.bar(airlines, average_lengths, color='maroon',
#         width=0.4)

####################################################    PLOT 6
response_klm, response_ba, response_other = average_response_time(tweets)
fig, ax = plt.subplots(ncols=3, nrows=1, sharey=True)
ax_1 =  sns.boxplot(data=response_klm, ax=ax[0])
ax_2 = sns.boxplot(data=response_ba, ax=ax[1])
ax_3 = sns.boxplot(data=response_other, ax=ax[2])
ax_1.set_ylim([0,400])



plt.show()



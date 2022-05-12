from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from main import *
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
languages, percentages = tweets_per_language(tweets)
explode = (0.1, 0, 0, 0)
fig1, ax1 = plt.subplots()
ax1.pie(percentages, explode = explode, labels=languages, autopct='%6.1f%%', # shows percentages in pie
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title("Distribution of languages of tweets", size=14)

# plt.title("Distribution of languages of tweets")
plt.show()

####################################################    PLOT 2
tweets_per_day_old = tweets_per_weekday(tweets)
tweets_per_day = [elem * 22 for elem in tweets_per_day_old]
categories = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

plt.bar(categories, tweets_per_day, color='maroon',
        width=0.4)
plt.xlabel("Day of the week")
plt.ylabel("Amount of tweets")
plt.title("Amount of tweets per day of the week")
plt.show()


####################################################    PLOT 3
sent_old, received_old = tweets_per_airline(tweets)
sent = [elem * 22 for elem in sent_old]
received = [elem * 22 for elem in received_old]
x = np.arange(3)
width = 0.40
plt.bar(x - 0.2, sent, width)
plt.bar(x + 0.2, received, width)
plt.ylabel("Amount of tweets")
plt.xlabel("KLM                  British Airways                   Others")
plt.title("Amount of total tweets per airline")
plt.legend(['Sent', 'Received'])
plt.show()

####################################################    PLOT 4
in_business_old, out_business_old = tweets_per_hour(tweets)
in_business = [elem * 22 for elem in in_business_old]
out_business = [elem * 22 for elem in out_business_old]

fig_4, ax_4 = plt.subplots(ncols=2, nrows=1)
ax_4_1 = sns.boxplot(data=in_business, ax=ax_4[0])
ax_4_2 = sns.boxplot(data=out_business, ax=ax_4[1])
ax_4_1.set_title("During business hours")
ax_4_2.set_title("Outside business hours")
ax_4_1.set_ylabel("Amount of tweets per hour")
fig_4.suptitle('Amount of tweets per hour during and outside of business hours', weight= 'bold')
plt.show()

####################################################    PLOT 5a
conversation_length_klm,\
conversation_length_ba,\
conversation_length_other = average_conversation_length(cleaned_conversations, tweets)

# sns.violinplot(data=conversation_length_klm)
# plt.show()
# sns.violinplot(data=conversation_length_ba)
# plt.show()
# sns.violinplot(data=conversation_length_other)
# plt.show()

fig, ax_8 = plt.subplots(ncols=3, nrows=1, sharey=True)
ax_8_1 = sns.violinplot(data=conversation_length_klm, ax=ax_8[0])
ax_8_2 = sns.violinplot(data=conversation_length_ba, ax=ax_8[1])
ax_8_3 = sns.violinplot(data=conversation_length_other, ax=ax_8[2])
ax_8_1.set_ylim([0, 20])
ax_8_1.set_title('KLM')
ax_8_2.set_title('BA')
ax_8_3.set_title('Others')
ax_8_1.set_ylabel("Conversation length (in tweets)")
fig.suptitle('Distribution of conversation length per airline', weight= 'bold', size=14)
plt.show()


####################################################    PLOT 5b  better?
# conversation_length_klm,\
# conversation_length_ba,\
# conversation_length_other = average_conversation_length(cleaned_conversations, tweets)
# airlines = ['KLM', 'BA', 'Other']
#
# average_lengths = [mean(conversation_length_klm), mean(conversation_length_ba), mean(conversation_length_other)]
# plt.bar(airlines, average_lengths, color='maroon',
#         width=0.4)
# plt.show()


####################################################    PLOT 6
response_klm, response_ba, response_other = average_response_time(tweets)
fig, ax_6 = plt.subplots(ncols=3, nrows=1, sharey=True)
ax_1 = sns.boxplot(data=response_klm, ax=ax_6[0])
ax_2 = sns.boxplot(data=response_ba, ax=ax_6[1])
ax_3 = sns.boxplot(data=response_other, ax=ax_6[2])
ax_1.set_ylim([0,400])
ax_1.set_title('KLM')
ax_2.set_title('BA')
ax_3.set_title('Others')
ax_1.set_ylabel("Response time (in minutes)")

fig.suptitle('Distributions of response times per airline', weight='bold', size=14)
plt.show()

# individual boxplots
# sns.boxplot(data=response_klm)
# plt.show()
# sns.boxplot(data=response_ba)
# plt.show()
# sns.boxplot(data=response_other)
# plt.show()

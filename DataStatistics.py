from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from datetime import datetime

def tweets_per_language(twt_list):
    """Tweets per language counter."""
    lang_freq_dict: dict = {'other': 0}
    counter = 0
    for i in range(len(twt_list)):
        if counter < 7:
            if twt_list[i]['lang'] in lang_freq_dict:
                lang_freq_dict[twt_list[i]['lang']] += 1
            else:
                lang_freq_dict[twt_list[i]['lang']] = 0
                counter += 1
        else:
            if twt_list[i]['lang'] in lang_freq_dict:
                lang_freq_dict[twt_list[i]['lang']] += 1
            else:
                lang_freq_dict['other'] += 1

    languages: list = []
    percentages: list = []

    for lang, freq in lang_freq_dict.items():
        languages.append(lang)
        percentages.append(freq/len(twt_list)*100)
    return languages, percentages

def tweets_per_weekday(twt_list):
    """Tweets per language counter."""
    monday_tweets = 0
    tuesday_tweets = 0
    wednesday_tweets = 0
    thursday_tweets = 0
    friday_tweets = 0
    saturday_tweets = 0
    sunday_tweets = 0
    tweet_count_per_day = []

    for i in range(len(twt_list)):
        weekday = datetime.weekday(datetime.fromtimestamp(int(twt_list[i]['timestamp_ms'])/1000))
        if weekday == 0:
            monday_tweets += 1
        if weekday == 1:
            tuesday_tweets += 1
        if weekday == 2:
            wednesday_tweets += 1
        if weekday == 3:
            thursday_tweets += 1
        if weekday == 4:
            friday_tweets += 1
        if weekday == 5:
            saturday_tweets += 1
        if weekday == 6:
            sunday_tweets += 1

    tweet_count_per_day.append(monday_tweets)
    tweet_count_per_day.append(tuesday_tweets)
    tweet_count_per_day.append(wednesday_tweets)
    tweet_count_per_day.append(thursday_tweets)
    tweet_count_per_day.append(friday_tweets)
    tweet_count_per_day.append(saturday_tweets)
    tweet_count_per_day.append(sunday_tweets)

    return tweet_count_per_day

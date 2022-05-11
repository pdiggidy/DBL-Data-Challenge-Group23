from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from datetime import datetime
from Lists import *
import statistics as stat


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
    """Tweets per language."""
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

def tweets_per_airline(twt_list):
    """Tweets sent and received per airline."""
    tweets_sent_klm = 0
    tweets_received_klm = 0
    tweets_sent_ba = 0
    tweets_received_ba = 0
    tweets_sent_other = 0
    tweets_received_other = 0

    for i in range(len(twt_list)):
        if int(twt_list[i]['user_id_str']) == klm_id:
            tweets_sent_klm += 1
        if int(twt_list[i]['user_id_str']) == ba_id:
            tweets_sent_ba += 1
        if int(twt_list[i]['user_id_str']) in airlines_list_wo_klm_wo_ba:
            tweets_sent_other += 1

        if str(klm_id) in twt_list[i]['user_mentions']:
            tweets_received_klm += 1
        if str(ba_id) in twt_list[i]['user_mentions']:
            tweets_received_ba += 1
        else:
            for airline in airlines_list_wo_klm_wo_ba:
                if str(airline) in twt_list[i]['user_mentions']:
                    tweets_received_other += 1

    sent = [tweets_sent_klm, tweets_sent_ba, tweets_sent_other/11]
    received = [tweets_received_klm, tweets_received_ba, tweets_received_other/11]

    # print(sent)
    # print(received)

    return sent, received

def tweets_per_hour(twt_list):
    """Tweest per hour of the day."""

    monday_tweets_in = 0
    tuesday_tweets_in = 0
    wednesday_tweets_in = 0
    thursday_tweets_in = 0
    friday_tweets_in = 0

    monday_tweets_out = 0
    tuesday_tweets_out = 0
    wednesday_tweets_out = 0
    thursday_tweets_out = 0
    friday_tweets_out = 0
    saturday_tweets_out = 0
    sunday_tweets_out = 0

    for i in range(len(twt_list)):
        if int(twt_list[i]['user_id_str']) == klm_id \
                or str(klm_id) in twt_list[i]['user_mentions'] \
                or twt_list[i]['in_reply_to_user_id_str'] == str(klm_id):
            weekday = datetime.weekday(datetime.fromtimestamp(int(twt_list[i]['timestamp_ms'])/1000))
            hour = datetime.fromtimestamp(int(twt_list[i]['timestamp_ms'])/1000).hour
            # print(weekday,hour)
            if weekday == 0:
                if 9 <= hour < 17:
                    monday_tweets_in += 1
                else:
                    monday_tweets_out += 1
            if weekday == 1:
                if 9 <= hour < 17:
                    tuesday_tweets_in += 1
                else:
                    tuesday_tweets_out += 1
            if weekday == 2:
                if 9 <= hour < 17:
                    wednesday_tweets_in += 1
                else:
                    wednesday_tweets_out += 1
            if weekday == 3:
                if 9 <= hour < 17:
                    thursday_tweets_in+= 1
                else:
                    thursday_tweets_out += 1
            if weekday == 4:
                if 9 <= hour < 17:
                    friday_tweets_in += 1
                else:
                    friday_tweets_out += 1
            if weekday == 5:
                saturday_tweets_out += 1
            if weekday == 6:
                sunday_tweets_out += 1

    in_business = [monday_tweets_in, tuesday_tweets_in, wednesday_tweets_in,
                   thursday_tweets_in, friday_tweets_in]
    out_business = [monday_tweets_out, tuesday_tweets_out, wednesday_tweets_out, thursday_tweets_out,
                    friday_tweets_out, saturday_tweets_out, sunday_tweets_out]

    print(in_business, out_business)
    return in_business, out_business

def average_conversation_length(conversations, twt_list):
    """Average conversation length."""
    conversation_length_klm = []
    conversation_length_ba = []
    conversation_length_other = []

    for convo in conversations:
        for i in range(len(twt_list)):
            if twt_list[i]['id_str'] == convo[0]:
                if twt_list[i]['user_id_str'] == klm_id \
                        or twt_list[i]['in_reply_to_user_id_str'] == klm_id \
                        or str(klm_id) in twt_list[i]['user_mentions']:
                    conversation_length_klm.append(len(convo))

                if twt_list[i]['user_id_str'] == ba_id \
                        or twt_list[i]['in_reply_to_user_id_str'] == ba_id \
                        or str(ba_id) in twt_list[i]['user_mentions']:
                    conversation_length_ba.append(len(convo))
                else:
                    conversation_length_other.append(len(convo))

    print(conversation_length_klm)
    print(conversation_length_ba)
    print(conversation_length_other)

    print(stat.mean(conversation_length_klm), stat.mean(conversation_length_ba), stat.mean(conversation_length_other))

    return conversation_length_klm, conversation_length_ba, conversation_length_other

def average_response_time(twt_list):
    """Average response time per airline."""
    response_times_klm = []
    response_times_ba = []
    response_times_other = []

    minute_times_klm = []
    minute_times_ba = []
    minute_times_other = []

    for i in range(len(twt_list)):
        if twt_list[i]['in_reply_to_status_id_str'] is not None:

            if int(twt_list[i]['user_id_str']) == klm_id:
                for j in range(len(twt_list)):
                    if twt_list[j]['id_str'] == twt_list[i]['in_reply_to_status_id_str']:
                        response_times_klm.append(abs(int(twt_list[i]['timestamp_ms']) - int(twt_list[j]['timestamp_ms'])))

            if int(twt_list[i]['user_id_str']) == ba_id:
                for j in range(len(twt_list)):
                    if twt_list[j]['id_str'] == twt_list[i]['in_reply_to_status_id_str']:
                        response_times_ba.append(abs(int(twt_list[i]['timestamp_ms']) - int(twt_list[j]['timestamp_ms'])))

            if int(twt_list[i]['user_id_str']) in airlines_list_wo_klm_wo_ba:
                for j in range(len(twt_list)):
                    if twt_list[j]['id_str'] == twt_list[i]['in_reply_to_status_id_str']:
                        response_times_other.append(abs(int(twt_list[i]['timestamp_ms']) - int(twt_list[j]['timestamp_ms'])))

    for time in response_times_klm:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_klm.append(time_object.hour*60 + time_object.minute)
    for time in response_times_ba:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_ba.append(time_object.hour*60 + time_object.minute)
    for time in response_times_other:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_other.append(time_object.hour*60 + time_object.minute)

    return minute_times_klm, minute_times_ba, minute_times_other

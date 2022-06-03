import os
from sqlalchemy import create_engine
from CompanySort import *
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from Lists import *
import statistics as stat
import seaborn as sns
import numpy as np

# My personal testing file :)


connection = create_engine(os.environ["DB_STRING"]).connect()


def sent_received():
    df_a = pd.DataFrame()
    for i in range(len(company_names)):
        df_a.loc[i, "Name"] = company_names[i]
        df_a.loc[i, "id"] = str(company_id_list[i])

    for j in range(len(df_a)):
        df_airline = pd.read_sql_table(df_a.loc[j, "Name"], connection)
        sent = 0
        received = 0
        for tw in range(len(df_airline)):
            if str(df_airline.loc[tw, "user_id_str"]) == df_a.loc[j, "id"]:
                sent += 1
            else:
                received += 1
        df_a.loc[j, "sent"] = sent
        df_a.loc[j, "received"] = received
    return df_a


def img_sent_received(df):
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_axes([0, 0, 1, 1])

    bar1 = ax.bar(df["Name"], df["received"], width=0.8, color="lightsteelblue", label="Tweets received")
    ax.bar(df["Name"], df["sent"], width=0.8, color="b", label="Tweets sent")
    plt.title("The amount of tweets sent and received per airline", size=16, weight="bold")
    plt.xlabel("Airline")
    plt.ylabel("Tweets")
    plt.legend(["Tweets received", "Tweets sent"])
    p=0
    for rect in bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{round(df.loc[p, "sent"] / df.loc[p, "received"] * 100, 1)}%', ha='center', va='bottom')
        p += 1
    plt.savefig('sent_received.png', bbox_inches='tight')


def day_week():
    df_dayweek = pd.DataFrame()
    monday, monday_klm = 0, 0
    tuesday, tuesday_klm = 0, 0
    wednesday, wednesday_klm = 0, 0
    thursday, thursday_klm = 0, 0
    friday, friday_klm = 0, 0
    saturday, saturday_klm = 0, 0
    sunday, sunday_klm = 0, 0

    df_al = pd.DataFrame()
    for i in range(len(company_names)):
        df_al.loc[i, "Name"] = company_names[i]
        df_al.loc[i, "id"] = str(company_id_list[i])

    for j in range(len(df_al)):
        KLM = False
        df_airline = pd.read_sql_table(df_al.loc[j, "Name"], connection)
        if str(df_al.loc[j, "id"]) == "56377143":
            KLM = True
        for tw in range(len(df_airline)):
            weekday = datetime.weekday(datetime.fromtimestamp(int(df_airline.loc[tw, "timestamp_ms"])/1000))
            if weekday == 0:
                monday += 1
                if KLM:
                    monday_klm += 1
            if weekday == 1:
                tuesday += 1
                if KLM:
                    tuesday_klm += 1
            if weekday == 2:
                wednesday += 1
                if KLM:
                    wednesday_klm += 1
            if weekday == 3:
                thursday += 1
                if KLM:
                    thursday_klm += 1
            if weekday == 4:
                friday += 1
                if KLM:
                    friday_klm += 1
            if weekday == 5:
                saturday += 1
                if KLM:
                    saturday_klm += 1
            if weekday == 6:
                sunday += 1
                if KLM:
                    sunday_klm += 1

    df_dayweek.loc["Monday", "Count"] = monday
    df_dayweek.loc["Monday", "Count_KLM"] = monday_klm
    df_dayweek.loc["Tuesday", "Count"] = tuesday
    df_dayweek.loc["Tuesday", "Count_KLM"] = tuesday_klm
    df_dayweek.loc["Wednesday", "Count"] = wednesday
    df_dayweek.loc["Wednesday", "Count_KLM"] = wednesday_klm
    df_dayweek.loc["Thursday", "Count"] = thursday
    df_dayweek.loc["Thursday", "Count_KLM"] = thursday_klm
    df_dayweek.loc["Friday", "Count"] = friday
    df_dayweek.loc["Friday", "Count_KLM"] = friday_klm
    df_dayweek.loc["Saturday", "Count"] = saturday
    df_dayweek.loc["Saturday", "Count_KLM"] = saturday_klm
    df_dayweek.loc["Sunday", "Count"] = sunday
    df_dayweek.loc["Sunday", "Count_KLM"] = sunday_klm
    return df_dayweek


def img_day_week(df):
        fig = plt.figure(figsize=(16, 9))
        ax = fig.add_axes([0, 0, 1, 1])

        bar2 = ax.bar(df.index, df["Count"], width=0.8, color="lightsteelblue", label="Total")
        bar3 = ax.bar(df.index, df["Count_KLM"], width=0.8, color="b", label="KLM")
        plt.title("The amount of tweets sent per weekday", size=16, weight="bold")
        plt.xlabel("Day")
        plt.ylabel("Tweets")
        plt.legend(["Total", "KLM"])
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        q = 0
        for rect in bar2:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{int(df.loc[days[q], "Count"])}', ha='center',
                     va='bottom')
            q += 1
        o = 0
        for rect in bar3:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{int(df.loc[days[o], "Count_KLM"])}', ha='center',
                     va='bottom')
            o += 1
        plt.savefig('day_week.png', bbox_inches='tight')

def tweets_per_hour():
    """Tweets per hour of the day."""

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

    df_a = pd.DataFrame()
    for i in range(len(company_names)):
        df_a.loc[i, "Name"] = company_names[i]
        df_a.loc[i, "id"] = str(company_id_list[i])

    for j in range(len(df_a)):
        df_airline = pd.read_sql_table(df_a.loc[j, "Name"], connection)
        for x in range(len(df_airline)):
            weekday = datetime.weekday(datetime.fromtimestamp(int(df_airline.loc[x, "timestamp_ms"])/1000))
            hour = datetime.fromtimestamp(int(df_airline.loc[x, "timestamp_ms"])/1000).hour

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

    print('in business is:')
    print(in_business)
    print('out business is:')
    print(out_business)
    return in_business, out_business


def img_tweets_per_hour(in_business, out_business):
    fig_4, ax_4 = plt.subplots(ncols=2, nrows=1, figsize=(16, 9), sharey=True)
    ax_4_1 = sns.boxplot(data=in_business, ax=ax_4[0])
    ax_4_2 = sns.boxplot(data=out_business, ax=ax_4[1])
    ax_4_1.set_title("During business hours")
    ax_4_2.set_title("Outside business hours")
    ax_4_1.set_ylabel("Amount of tweets per hour")
    ax_4_1.set_xlabel("")
    ax_4_2.set_xlabel("")
    fig_4.suptitle('Amount of tweets per hour during and outside of business hours', weight='bold')
    plt.savefig("twperhour.png", bbox_inches='tight')


def avg_conv_length():
    conversation_length_klm = []
    conversation_length_ba = []
    conversation_length_other = []
    df_conv = pd.read_sql_table("Conversations", connection)
    for i in range(1, 49):
        df_conv[str(i)] = df_conv[str(i)].astype("str")
    df_klm = pd.read_sql_table("KLM", connection)
    df_klm["id_str"] = df_klm["id_str"].astype("str")
    df_ba = pd.read_sql_table("BritishAirways", connection)
    df_ba["id_str"] = df_ba["id_str"].astype("str")
    for i in range(len(df_conv)):
        #print(i)
        convlen = 0
        for x in range(50):
            if df_conv.iloc[i, x] == "0":
                convlen = x - 1
                break
        if df_conv.loc[i, "1"] == "1130822387044442112":
            print("a")
        if df_conv.loc[i, "1"] == 1130822387044442112:
            print("b")
        if df_conv.loc[i, "1"] in df_klm["id_str"]:
            conversation_length_klm.append(convlen)
        elif df_conv.loc[i, "1"] in df_ba["id_str"]:
            conversation_length_ba.append(convlen)
        else:
            conversation_length_other.append(convlen)
    print(conversation_length_klm)
    print(conversation_length_ba)

# df_sent_received = sent_received()
# print(df_sent_received)
# img_sent_received(df_sent_received)
# df_dw = day_week()
# print(df_dw)
# img_day_week(df_dw)
# intw, outtw = tweets_per_hour()
# img_tweets_per_hour(intw, outtw)
avg_conv_length()


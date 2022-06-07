import os
from sqlalchemy import create_engine
from CompanySort import *
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
import math as math
from Lists import *
import statistics
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
    klm_set = set(df_klm["id_str"])
    ba_set = set(df_ba["id_str"])
    for i in range(len(df_conv)):
        print(i)
        convlen = 0
        for x in range(50):
            if df_conv.iloc[i, x] == "0":
                convlen = x
                break

        if df_conv.loc[i, "1"] in klm_set:
            conversation_length_klm.append(convlen)
        elif df_conv.loc[i, "1"] in ba_set:
            conversation_length_ba.append(convlen)
        else:
            conversation_length_other.append(convlen)
    return conversation_length_klm, conversation_length_ba, conversation_length_other


def img_avg_conv_length(conversation_length_klm, conversation_length_ba, conversation_length_other):
    fig, ax_8 = plt.subplots(ncols=3, nrows=1, sharey=True)
    ax_8_1 = sns.violinplot(data=conversation_length_klm, ax=ax_8[0])
    ax_8_2 = sns.violinplot(data=conversation_length_ba, ax=ax_8[1])
    ax_8_3 = sns.violinplot(data=conversation_length_other, ax=ax_8[2])
    ax_8_1.set_ylim([0, 10])
    ax_8_1.set_title('KLM')
    ax_8_2.set_title('BA')
    ax_8_3.set_title('Others')
    ax_8_1.set_ylabel("Conversation length (in tweets)")
    fig.suptitle('Distribution of conversation length per airline', weight='bold', size=14)
    plt.savefig("avg_conv_len.png", bbox_inches='tight')


def resp_time():

    query_klm = """
    SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
        FROM All_tweets BASIS
            INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str  = 56377143           
    """

    query_ba = """
        SELECT REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
            FROM All_tweets BASIS
                INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str  = 18332190        
        """

    query_ej = """
            SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
                FROM All_tweets BASIS
                    INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                    38676903  
            """

    query_ra = """
     SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
        FROM All_tweets BASIS
                INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                1542862735 
    """

    query_af = """
         SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
            FROM All_tweets BASIS
                    INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                    106062176 
        """

    query_aa = """
             SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
                FROM All_tweets BASIS
                        INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                        22536055 
            """

    query_lh = """
                 SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
                    FROM All_tweets BASIS
                            INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                            124476322 
                """

    query_sa = """
                     SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
                        FROM All_tweets BASIS
                                INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                                253340062 
                    """

    query_qt = """
                         SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
                            FROM All_tweets BASIS
                                    INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                                    218730857 
                        """

    query_et = """
                             SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
                                FROM All_tweets BASIS
                                        INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                                        45621423 
                            """

    query_va = """
                                 SELECT REPLY.user_id_str, REPLY.timestamp_ms - BASIS.timestamp_ms AS DiffTimeStamp
                                    FROM All_tweets BASIS
                                            INNER JOIN All_tweets REPLY on REPLY.in_reply_to_status_id_str = BASIS.id_str AND REPLY.user_id_str =
                                            20626359 
                                """
    minute_times_klm = []
    minute_times_ba = []
    minute_times_ej = []
    minute_times_ra = []
    minute_times_af = []
    minute_times_aa = []
    minute_times_lh = []
    minute_times_sa = []
    minute_times_qt = []
    minute_times_et = []
    minute_times_va = []
    df_klm = pd.read_sql_query(query_klm, connection)
    df_ba = pd.read_sql_query(query_ba, connection)
    df_ej = pd.read_sql_query(query_ej, connection)
    df_ra = pd.read_sql_query(query_ra, connection)
    df_af = pd.read_sql_query(query_af, connection)
    df_aa = pd.read_sql_query(query_aa, connection)
    df_lh = pd.read_sql_query(query_lh, connection)
    df_sa = pd.read_sql_query(query_sa, connection)
    df_qt = pd.read_sql_query(query_qt, connection)
    df_et = pd.read_sql_query(query_et, connection)
    df_va = pd.read_sql_query(query_va, connection)
    response_times_klm = list(df_klm["DiffTimeStamp"])
    response_times_ba = list(df_ba["DiffTimeStamp"])
    response_times_ej = list(df_ej["DiffTimeStamp"])
    response_times_ra = list(df_ra["DiffTimeStamp"])
    response_times_af = list(df_af["DiffTimeStamp"])
    response_times_aa = list(df_aa["DiffTimeStamp"])
    response_times_lh = list(df_lh["DiffTimeStamp"])
    response_times_sa = list(df_sa["DiffTimeStamp"])
    response_times_qt = list(df_qt["DiffTimeStamp"])
    response_times_et = list(df_et["DiffTimeStamp"])
    response_times_va = list(df_va["DiffTimeStamp"])

    for time in response_times_klm:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_klm.append(time_object.hour*60 + time_object.minute)
    for time in response_times_ba:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_ba.append(time_object.hour*60 + time_object.minute)
    for time in response_times_ej:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_ej.append(time_object.hour*60 + time_object.minute)
    for time in response_times_ra:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_ra.append(time_object.hour*60 + time_object.minute)
    for time in response_times_af:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_af.append(time_object.hour*60 + time_object.minute)
    for time in response_times_aa:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_aa.append(time_object.hour*60 + time_object.minute)
    for time in response_times_lh:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_lh.append(time_object.hour*60 + time_object.minute)
    for time in response_times_sa:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_sa.append(time_object.hour*60 + time_object.minute)
    for time in response_times_qt:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_qt.append(time_object.hour*60 + time_object.minute)
    for time in response_times_et:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_et.append(time_object.hour*60 + time_object.minute)
    for time in response_times_va:
        time_object = datetime.fromtimestamp(time/1000)
        minute_times_va.append(time_object.hour*60 + time_object.minute)

    return minute_times_klm, minute_times_ba, minute_times_ej, minute_times_ra, minute_times_af, minute_times_aa, minute_times_lh, minute_times_sa, minute_times_qt, minute_times_et, minute_times_va


def img_resp_time(response_klm, response_ba, response_ej, response_ra, response_af, response_aa, response_lh, response_sa, response_qt, response_et, response_va):
    fig, ax_6 = plt.subplots(ncols=11, nrows=1, sharey=True, figsize=(16, 9))
    ax_1 = sns.violinplot(data=response_klm, ax=ax_6[0])
    ax_2 = sns.violinplot(data=response_ba, ax=ax_6[1])
    ax_3 = sns.violinplot(data=response_ej, ax=ax_6[2])
    ax_4 = sns.violinplot(data=response_ra, ax=ax_6[3])
    ax_5 = sns.violinplot(data=response_af, ax=ax_6[4])
    ax_61 = sns.violinplot(data=response_aa, ax=ax_6[5])
    ax_7 = sns.violinplot(data=response_lh, ax=ax_6[6])
    ax_8 = sns.violinplot(data=response_sa, ax=ax_6[7])
    ax_9 = sns.violinplot(data=response_qt, ax=ax_6[8])
    ax_10 = sns.violinplot(data=response_et, ax=ax_6[9])
    ax_11 = sns.violinplot(data=response_va, ax=ax_6[10])
    ax_1.set_ylim(0, 400)
    ax_1.set_title('KLM')
    ax_2.set_title('BA')
    ax_3.set_title('EJ')
    ax_4.set_title("RA")
    ax_5.set_title("AF")
    ax_61.set_title("AA")
    ax_7.set_title("LH")
    ax_8.set_title("SA")
    ax_9.set_title("QT")
    ax_10.set_title("ET")
    ax_11.set_title("VA")
    ax_1.set_ylabel("Response time (mins)")
    fig.suptitle('Distributions of response times per airline', weight='bold', size=14)
    plt.savefig("resp_time.png", bbox_inches='tight')

#def fun():


# df_sent_received = sent_received()
# print(df_sent_received)
# img_sent_received(df_sent_received)

# df_dw = day_week()
# print(df_dw)
# img_day_week(df_dw)

# intw, outtw = tweets_per_hour()
# img_tweets_per_hour(intw, outtw)

# a, b, c = avg_conv_length()
# img_avg_conv_length(a, b, c)

d, e, f, g, h, i, j, k, l, m, n = resp_time()
img_resp_time(d, e, f, g, h, i, j, k, l, m, n)


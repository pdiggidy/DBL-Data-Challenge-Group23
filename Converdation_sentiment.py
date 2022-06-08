import os
from sqlalchemy import create_engine
from CompanySort import *
import pandas as pd


def add_properties_to_conversations():
    """Reformats the conversations so that each tweet in the conversations will have acces to it's
    user_id and sentiment value. Also adds the conv_id and msg_nr."""
    connection = create_engine(os.environ["DB_STRING"]).connect()
    df_conv = pd.DataFrame()
    for x in range(1, 16):
        print(x)
        q = f"""
        SELECT Con.{x} as tweet_id, AT.user_id_str as user_id, {x} as msg_nr, Con.index as conv_id, AT.sentiment as sentiment
            FROM  Conversations_max_15 Con
            INNER JOIN All_tweets_labeled AT on Con.{x} = AT.id_str
        """

        df_t = pd.read_sql_query(q, connection)
        df_conv = pd.concat([df_conv, df_t], ignore_index=True)

    df_conv = df_conv.set_index(["conv_id", "msg_nr"])
    df_conv = df_conv.sort_index()
    connection.close()
    return df_conv


df_conv = add_properties_to_conversations()
print(df_conv)

##### Save table to SQL server
# connection = create_engine(os.environ["DB_STRING"]).connect()
# df_conv.to_sql("Conversations_updated", connection, schema="Tweets_Data", if_exists="fail")
# connection.close()


def split_conversation_per_user():
    """Gets the conversations from SQL server, and splits each conversation into relevant
    sequences of tweets of specific users. If KLM has replied to a user within a conversation, then all the
    tweets of this user within this conversation will form a new sequence of tweets."""
    connection = create_engine(os.environ["DB_STRING"]).connect()
    querrry = """SELECT *
                FROM Conversations_updated
                """
    df = pd.read_sql_query(querrry, connection)
    df_sentiment = pd.read_sql_query("SELECT id_str, sentiment FROM All_tweets_labeled", connection, index_col="id_str")
    connection.close()

    tweetID_sentiment = df_sentiment["sentiment"].to_dict()
    all_tweets_conv = []

    for i in range(1, df.iloc[-1, 0] + 1):
        conversation = df[df["conv_id"] == i].to_numpy()
        players = set()
        for j in range(1, len(conversation)):
            tweet = conversation[j]
            msg_nr, tweet_id, user_id = tweet[1], tweet[2], tweet[3]

            if user_id in company_id_list:  # equal to klm
                prev_tweet = conversation[j - 1]  # ?check bounds?
                prev_user_id = prev_tweet[3]
                players.add(prev_user_id)
        if not (players):
            continue

        players_tweets = {}
        for n in range(len(conversation)):
            tweet = conversation[n]
            msg_nr = tweet[1]
            tweet_id = tweet[2]
            user_id = tweet[3]
            if user_id in players:
                players_tweets[user_id] = players_tweets.get(user_id, []) + [tweet_id]
        conv_tweets = [players_tweets[user_id] for user_id in players_tweets if len(players_tweets[user_id]) > 1]
        all_tweets_conv.extend(conv_tweets)

    df_conv_id_str = pd.DataFrame(all_tweets_conv).fillna(0).astype("int64")
    df_conv_SA = pd.DataFrame([list(map(lambda x: tweetID_sentiment[x], conv)) for conv in all_tweets_conv]).fillna(0)
    return df_conv_id_str, df_conv_SA


df_conv_id_str, df_conv_SA = split_conversation_per_user()

##### Save tables to SQL server
# connection = create_engine(os.environ["DB_STRING"]).connect()
# df_end_conv_id_str.to_sql("Conversations_id_str_for_SA", connection, schema="Tweets_Data", if_exists="fail")
# df_end_conv_SA.to_sql("Conversations_sentiment_for_SA", connection, schema="Tweets_Data", if_exists="fail")
# connection.close()




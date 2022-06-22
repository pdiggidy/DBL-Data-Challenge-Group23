from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
from typing import List
from Lists import *


def conversations_list_builder(twt_list, conversations=[]) -> List[list]:
    """"Creates conversation lists from tweet dictionary input."""
    for i in range((len(twt_list)-1),-1,-1):  # loop through the tweets reversely
        if twt_list[i]['in_reply_to_status_id_str'] is not None \
           and int(twt_list[i]['in_reply_to_user_id_str']) in airlines_list \
           or int(twt_list[i]['user_id_str']) in airlines_list \
           and twt_list[i]['in_reply_to_status_id_str'] is not None:
                # tweet is in reply to another tweet (1)
                # AND
                # other tweet is from an airline (1)
                # OR
                # tweet is from an airline (2)
                # AND
                # it is replying to another tweet (2)

            convo_nr = 0                # iterator for the while loop
            in_conversations = False   # false as long as tweet does not already exist in our conversations

            for convo in conversations:
                if twt_list[i]['id_str'] == convo[-1]:
                    convo.append(twt_list[i]['in_reply_to_status_id_str'])
                    in_conversations = True  # tweet is found, so true

            if not in_conversations:   # if the tweet has not been found somewhere in our conversations
                conversations.append([twt_list[i]['id_str'], twt_list[i]['in_reply_to_status_id_str']])
                                       # add the tweet and the tweet it is replying to, to our conversations

    return conversations


def conversations_cleaner(conversations_to_clean: List[list]) -> List[list]:
    """"Removes non conversations (less than 3 tweets) from collected interactions."""
    cleaned_conversations: List[list] = []            # will hold the "cleaned" conversations

    for convo in conversations_to_clean:
        if len(convo) >= 3:                           # our definition of a conversation (at least 3 tweets)
            cleaned_conversations.append(convo)       # add the conversation to our new conversations list

    return cleaned_conversations


def conversations_list_to_df(conversations: List[list]) -> pd.DataFrame:
    """"Creates conversation dataframes from tweet dictionary."""
    conversations_df = pd.DataFrame(conversations)    # makes a DataFrame out of our list of lists (conversations)
    conversations_df_indexed = pd.DataFrame(conversations, index=conversations_df.iloc[:, 0])
                                                      # makes a new DataFrame where the index is the last reply
    del conversations_df_indexed[0]                   # remove the now redundant and duplicant column

    return conversations_df_indexed

def conversation_builder(df: pd.DataFrame):
    """Create conversation dataframes from tweets dataframe."""
    all_tweetID: set = set(df.index)    # alle tweets (exl dubbel)
    tweetID_replytotweetID: dict = df["in_reply_to_status_id_str"].dropna().to_dict()
    tweetID_userID = df["user_id_str"].to_dict()

    replies_tweetID: set = set(tweetID_replytotweetID.keys())       # tweets met IRT (exl dubbel)
    parent_tweetID: set = set(tweetID_replytotweetID.values())      # tweets that have a reply
    children_tweetID = replies_tweetID.difference(parent_tweetID)   # tweets that ARE replies

    all_conversations = []

    # start a conversation from each Conversation Starter
    for id_str in children_tweetID:
        conversation = []

        # compile a whole conversation from bottom to top
        while True:
            conversation.append(id_str)                             # CBA
            id_str = tweetID_replytotweetID.get(id_str, None)       # id=B, id=A, id=None
            if not id_str:  # if not None                           # 001
                break

        # reverse the conversation so the first tweet will be in the first row.
        conversation.reverse()

        # only keep conversations with at least 2 people
        people = set()
        less_than_1_person = True
        for i in range(len(conversation)):
            tweet_id = conversation[i]
            user_id_str = tweetID_userID.get(tweet_id)
            if user_id_str is None:
                break
            people.add(user_id_str)
            if len(people) > 1:
                less_than_1_person = False
                break
        if less_than_1_person:
            continue

        # only append conversations that are between 3 and 50 tweets long, and for which all tweet data is available
        if 2 < len(conversation) < 15 and conversation[0] in all_tweetID:
            all_conversations.append(conversation)

    conversations_df = pd.DataFrame(all_conversations, columns=range(1, 1+len(max(all_conversations, key=len))))
    return conversations_df


def create_newest_raw_conversation(table_name):
    """Take older conversation version and update it."""

    connection = create_engine(os.environ["DB_STRING"]).connect()

    # create raw dataframe
    q = f"""SELECT conv_id, msg_nr, user_id, tweet_id, sentiment
           FROM {table_name} LIMIT 10000
        """
    df_raw_conv = pd.read_sql_query(q, connection).set_index(["conv_id", "msg_nr"])
    df_raw_conv.insert(0, "inter_nr", -1)
    df_raw_conv.insert(2, "is_airline", df_raw_conv["user_id"].isin(airlines_list))

    connection.close()

    tweetid_to_internr = {}

    for conv_id in df_raw_conv.index.get_level_values("conv_id"):  # iterate over each conversation
        df_short = df_raw_conv.loc[conv_id, :]
        mentioned_users = []  # keep track of users that have been replied to by airline in conversation
        relevant_users = []  # keep track of the users that tweeted after being replied to

        for msg_nr in df_short.index:  # iterate over each tweet in the conversation
            cur_user_id = df_short.loc[msg_nr, "user_id"]  # user_id of current tweet

            # if current user is an airline, then add previous user to relevant users
            if cur_user_id in airlines_list and msg_nr != 1:
                prev_user_id = df_short.loc[msg_nr - 1, "user_id"]
                if cur_user_id != prev_user_id:  # don't add if previous user is also an airline
                    if prev_user_id not in mentioned_users:
                        mentioned_users.append(prev_user_id)

            # if a user tweets, and have been previously tweeted to by an airline, add him to relevant users
            elif cur_user_id in mentioned_users:
                if cur_user_id not in relevant_users:
                    relevant_users.append(cur_user_id)

        # get the relevant users in the right order (the one who tweeted first, is first due to inter_nr)
        relevant_users_ordered = [i for i in mentioned_users if i in relevant_users]

        # calculate the last index of the conversation (so you can make sure you won't get out of bound)
        end_index = len(df_short)

        # collect the inter_nr for each relevant tweet
        for msg_nr in df_short.index:  # iterate over each tweet in the conversation
            cur_user_id = df_short.loc[msg_nr, "user_id"]  # user_id of current tweet

            # determine tweet_id when we're at the right tweets and add those and the internmr to dict
            if cur_user_id in relevant_users_ordered:
                cur_tweet_id = df_short.loc[msg_nr, "tweet_id"]
                tweetid_to_internr[cur_tweet_id] = relevant_users_ordered.index(cur_user_id) + 1

                # also check if next tweet is the airline and add him to the same interaction
                if msg_nr < end_index - 1:
                    user_next_msg = df_short.loc[msg_nr + 1, "user_id"]
                    if user_next_msg in airlines_list:
                        cur_tweet_id = df_short.loc[msg_nr + 1, "tweet_id"]
                        tweetid_to_internr[cur_tweet_id] = relevant_users_ordered.index(cur_user_id) + 1

    # map the tweet_id's to interaction number
    df_raw_conv["inter_nr"] = df_raw_conv["tweet_id"].apply(lambda tweet_id: tweetid_to_internr[tweet_id]
    if tweetid_to_internr.get(tweet_id) else -1)

    # set the MultiIndex
    df_raw_conv.set_index("inter_nr", append=True, inplace=True)
    df_raw_conv.reorder_levels(["conv_id", "inter_nr", "msg_nr"])

    return df_raw_conv


def create_newest_filtered_conversation(df_raw_conv: pd.DataFrame):
    """Take the newest raw conversation and format it to get conversations ready for sentiment analysis.
    """
    # reset the index
    df_raw_conv.reset_index("msg_nr", inplace=True)

    # first filter: remove all tweets that have not been given an inter_nr (so are not relevant for sentiment)
    interactions_df = df_raw_conv[df_raw_conv.index.get_level_values("inter_nr") != -1]

    # second filter: remove all interactions that have less than 2 tweets of the unique user
    interactions_without_air_df = interactions_df[interactions_df["is_airline"] == False]
    index_conv_id = interactions_without_air_df.index
    msg_count = index_conv_id.value_counts(sort=False)
    # only keep interactions that future the user at least 2 times
    needed_index_conv_id = [i for i, count in msg_count.iteritems() if count > 1]
    interactions_filt_df = interactions_df.loc[needed_index_conv_id, :]

    # add the inter_nr to the index
    df_raw_conv.set_index("msg_nr", append=True, inplace=True)
    interactions_filt_df.set_index("msg_nr", append=True, inplace=True)

    return interactions_filt_df

df_raw_conv = create_newest_raw_conversation("Conversations_max_15_updated")
interactions_filt_df = create_newest_filtered_conversation(df_raw_conv)
6
# df_raw_conv.to_sql("Conversations_Newest_All", connection, schema="Tweets_Data", if_exists="fail")
# interactions_filt_df.to_sql("Conversations_Newest_SA_incl_airline", connection, schema="Tweets_Data", if_exists="fail")
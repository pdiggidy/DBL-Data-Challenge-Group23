import pandas as pd
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
    all_tweetID: set = set(df.index)    # alle tweets (exl dubbel)
    tweetID_replytotweetID: dict = df["in_reply_to_status_id_str"].dropna().to_dict()
    tweetID_userID: pd.Series = df["user_id_str"].to_dict()

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
        if 2 < len(conversation) < 50 and conversation[0] in all_tweetID:
            all_conversations.append(conversation)

    conversations_df = pd.DataFrame(all_conversations, columns=range(1, 1+len(max(all_conversations, key=len))))
    return conversations_df





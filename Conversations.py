import pandas as pd
from typing import List
from Lists import *


def conversations_list_builder(twt_list) -> List[list]:
    """"Creates conversation lists from tweet dictionary input."""
    conversations: List[list]= []             # will hold the conversations
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

            list_nr = 0                # iterator for the while loop
            in_conversations = False   # false as long as tweet does not already exist in our conversations

            while list_nr < len(conversations):       # iterate through the conversation list
                for elem in conversations[list_nr]:   # for every tweet in a conversation
                    if elem == twt_list[i]['id_str']: # if the tweet (id) has been found in a conversation in our list
                        conversations[list_nr].append(twt_list[i]['in_reply_to_status_id_str'])
                                                      # add the tweet it is replying to, to the conversation
                        in_conversations = True       # tweet is found, so true
                list_nr += 1                          # increase iterator

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
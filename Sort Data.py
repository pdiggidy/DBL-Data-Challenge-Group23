import pandas as pd
import numpy as np
import json
import os
from typing import List, Dict, Set, Tuple
from Lists import *
from CompanySort import *


def create_dictionaries(filepath: str) -> Tuple[List[dict], Dict[str, dict], Dict[str, tuple]]:
    """Creates 3 dictionaries from given json file path: tweets, users and updated_counts.
    """
    tweets: List[dict] = []
    users: Dict[str, dict] = dict()
    updated_counts: Dict[str, Tuple] = dict()

    with open(filepath, "r") as file:
        for line in file:
            # load the json file in a dictionary and handle errors
            tweet: dict = create_raw_tweet(line)

            # create dictionary with updated counts of quotes, replies, retweets and likes
            rt_count, qt_count = update_counts(tweet)

            # continue to next tweet if tweet is deleted or a retweet
            if ("delete" in tweet) or ("retweeted_status" in tweet):
                continue

            # for extended tweets: replace full_text,entities and text_range attributes
            extended_tweet_handler(tweet)

            # extract hashtags and user_mentions from entities and make separate columns of them
            entities_handler(tweet)
            # extract latitude and longitude from coordinates and make separate columns of them
            coordinates_handler(tweet)

            #Assign each tweet to one or more companies
            tweet["company"] = find_company(company_id_list, company_names, tweet)

            # only keep text within "display_text_range" bounds
            cut_text(tweet)

            # extract user dictionary and replace with user_id_str
            user_info: dict = extract_user(tweet)

            # remove abundant attributes from dictionaries
            remove_attributes(tweet, remove_tweet_attr)
            remove_attributes(user_info, remove_user_info_attr)
            remove_attributes(tweet["place"], remove_tweet_place_attr)

            # combine dictionaries of this tweet with other dictionaries
            tweets.append(tweet)
            users[user_info.pop("id_str")] = user_info
            updated_counts.update(rt_count)
            updated_counts.update(qt_count)

    return tweets, users, updated_counts


def create_dataframes(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Creates 3 dataframes from given json file path: tweets, users and updated_counts.
    """
    # create 3 collections of dictionaries
    tweets, users, updated_counts = create_dictionaries(filepath)

    # create 3 dataframes
    df_tweets = pd.DataFrame(tweets)

    df_users = pd.DataFrame.from_dict(users, orient='index')
    df_users.index.name = "user_id_str"

    updates_columns: list = ["quote_count", "reply_count", "retweet_count", "favorite_count"]
    df_updated_counts = pd.DataFrame.from_dict(updated_counts, columns=updates_columns, orient="index")

    df_tweets = df_tweets[df_tweets.company.notnull()]

    return df_tweets, df_users, df_updated_counts


def create_raw_tweet(line: str) -> dict:
    """Created dictionary from json text line and return it. Avoid errors like "Exceeded
    connection limit for user" by returning a deleted tweet.
    """
    try:
        tweet: dict = json.loads(line)  # load the line into a dictionary to represent one tweet
    except json.decoder.JSONDecodeError:
        tweet = {"delete": True}  # return a deleted tweet if there is an error

    return tweet


def extract_user(tweet: dict) -> dict:
    """Extract user dictionary and replace it with user_id_str. Also return the user dictionary.
    """
    user_info: dict = tweet.pop("user")  # store user info in a separate dictionary
    tweet["user_id_str"] = user_info["id_str"]
    return user_info


def remove_attributes(dictionary: dict, remove: List[str]) -> None:
    """Remove attributes from given dictionary.
    """
    if type(dictionary) == dict:
        for column_name in remove:
            dictionary.pop(column_name, None)


def update_counts(tweet: dict) -> Tuple[dict, dict]:
    """In case retweet or quote tweet, return updated values of referenced tweet:
    {status_id: (quote_count, reply_count, retweet_count and favorite_count)}
    """
    rt_count_dict, qt_count_dict = {}, {}  # rt=retweet,  qt=quoted tweet

    if "retweeted_status" in tweet:
        rt: dict = tweet["retweeted_status"]
        rt_id: str = rt["id_str"]
        rt_count: tuple = rt["quote_count"], rt["reply_count"], rt["retweet_count"], rt["favorite_count"]
        rt_count_dict: Dict[str, tuple] = {rt_id: rt_count}

    if "quoted_status" in tweet:
        qt: dict = tweet["quoted_status"]
        qt_id: str = qt["id_str"]
        qt_count: tuple = qt["quote_count"], qt["reply_count"], qt["retweet_count"], qt["favorite_count"]
        qt_count_dict: Dict[str, tuple] = {qt_id: qt_count}

    return rt_count_dict, qt_count_dict


def extended_tweet_handler(tweet: dict) -> None:
    """In case of a tweet that has more characters than was initially allowed by twitter:
    Restore the tweet with it's full text, entities and text_range.
    """
    if "extended_tweet" in tweet:
        tweet["text"] = tweet["extended_tweet"]["full_text"]
        tweet["display_text_range"] = tweet["extended_tweet"]["display_text_range"]
        tweet["entities"] = tweet["extended_tweet"]["entities"]
        del tweet["extended_tweet"]


def coordinates_handler(tweet: dict) -> None:
    """Separates "coordinates" content (latitude and longitude) into different columns.
    """
    if tweet["coordinates"]:
        tweet["latitude"] = tweet["coordinates"]["coordinates"][1]
        tweet["longitude"] = tweet["coordinates"]["coordinates"][0]


def entities_handler(tweet: dict) -> None:
    """Separates "entities" content (hashtags and user_mentions) into different columns.
    """
    hashtags: list = [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]]
    user_mentions: list = [user_mention["id_str"] for user_mention in tweet["entities"]["user_mentions"]]

    tweet["hashtags"] = np.array(hashtags)
    tweet["user_mentions"] = np.array(user_mentions)


def cut_text(tweet: dict) -> None:
    """Remove abundant text of the tweet by shortening the text to the "display_text_range" bounds
    """
    if "display_text_range" in tweet:
        begin, end = tweet["display_text_range"]
        tweet["text"] = tweet["text"][begin:end]


def conversations_dict_builder(twt_list) -> List[list]:
    """"Creates conversation lists from tweet dictionary input."""
    conversations: List[list]= []
    for i in range((len(twt_list)-1),-1,-1):
        if twt_list[i]['in_reply_to_user_id_str'] is not None \
                and int(twt_list[i]['in_reply_to_user_id_str']) in airlines_list \
                or int(twt_list[i]['user_id_str']) in airlines_list:
            list_nr = 0
            in_conversations = False

            while list_nr < len(conversations):
                for elem in conversations[list_nr]:
                    if elem == twt_list[i]['id_str']:
                        conversations[list_nr].append(twt_list[i]['in_reply_to_status_id_str'])
                        in_conversations = True
                list_nr += 1

            if not in_conversations:
                conversations.append([twt_list[i]['id_str'], twt_list[i]['in_reply_to_status_id_str']])

    return conversations

def conversation_dict_to_df(conversations: List[list]) -> pd.DataFrame:
    """"Creates conversation dataframes from tweet dictionary"""
    conversations_df = pd.DataFrame(conversations)
    conversations_df_indexed = pd.DataFrame(conversations, index=conversations_df.iloc[:, 0])
    del conversations_df_indexed[0]
    return conversations_df_indexed


# creating dataframes from json files
tweets, users, updated_counts = create_dictionaries("data/airlines-1558611772040.json")
tweets_df, users_df, updated_counts_df = create_dataframes("data/airlines-1558611772040.json")

# creating conversation dataframes
conversations = conversations_dict_builder(tweets)
conversations_df = conversation_dict_to_df(conversations)

# for debugging purposes
print(tweets_df)
print("place count: ", tweets_df["place"].count())
print(conversations_df)


# def run_data_directory():
#     """Run with all data in 'data' directories"""
#     tweets_dfs, users_dfs, updated_counts_dfs = [], [], []
#     for filename in os.listdir("data"):
#         path_name = os.path.join("data", filename)
#         tweets_frame, users_frame, updated_counts_frame = create_dataframes(path_name)
#         tweets_dfs.append(tweets_frame)
#         users_dfs.append(users_frame)
#         updated_counts_dfs.append(updated_counts_frame)
#     return tweets_dfs, users_dfs, updated_counts_dfs
# print([len(df) for dfs in run_data_directory() for df in dfs])

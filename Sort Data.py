import pandas as pd
import numpy as np
import json
import os
from typing import List, Dict, Set, Tuple
from remove_lists import *
from CompanySort import *


def create_dictionaries(filepath: str) -> Tuple[List[dict], Dict[str, dict], Dict[str, tuple]]:
    """Creates 3 dictionaries from given json file path: tweets, users and updated_counts."""
    tweets: List[dict] = []
    users: Dict[str, dict] = dict()
    updated_counts: Dict[str, Tuple] = dict()

    with open(filepath, "r") as file:
        for line in file:
            # load the json file in a dictionary
            tweet: dict = create_raw_tweet(line)
            if not tweet:  # continue if "Exceeded connection limit" error
                continue

            # create dictionary with updated counts of quotes, replies, retweets
            # and likes (before removing quoted_status attr)
            rt_count, qt_count = update_counts(tweet)

            # continue to next tweet if tweet is deleted or a retweet
            if ("delete" in tweet) or ("retweeted_status" in tweet):
                continue

            # replace full_text,entities and text_range for extended tweets
            extended_tweet_handler(tweet)

            # make separate columns of entities and coordinates
            entities_handler(tweet)
            coordinates_handler(tweet)

            # only keep text in display_text_range
            cut_text(tweet)

            # extract user dictionary and replace with user_id_str
            user_info: dict = extract_user(tweet)

            # remove abundant attributes from dictionaries
            remove_attributes(tweet, remove_tweet_attr)
            remove_attributes(user_info, remove_user_info_attr)
            remove_attributes(tweet["place"], remove_tweet_place_attr)

            # add dictionary to the rest
            tweets.append(tweet)
            users[user_info.pop("id_str")] = user_info
            updated_counts.update(rt_count)
            updated_counts.update(qt_count)

    return tweets, users, updated_counts


def create_dataframes(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Creates 3 dataframes from given json file path: tweets, users and updated_counts.
    """
    tweets, users, updated_counts = create_dictionaries(filepath)

    df_tweets = pd.DataFrame(tweets)
    df_users = pd.DataFrame.from_dict(users, orient='index')
    df_users.index.name = "user_id_str"
    updates_columns: list = ["quote_count", "reply_count", "retweet_count", "favorite_count"]
    df_updated_counts = pd.DataFrame.from_dict(updated_counts, columns=updates_columns, orient="index")

    return df_tweets, df_users, df_updated_counts


def create_raw_tweet(line: str) -> dict:
    """Create dictionary from json text line. Avoid the 'Exceeded connection limit' error by returning None.
    """
    try:
        tweet: dict = json.loads(line)
    except json.decoder.JSONDecodeError:
        tweet = None
        if line != "Exceeded connection limit for user\n":
            raise NameError(f'json load error with line: {line}')
    return tweet


def extract_user(tweet: dict) -> dict:
    """Extract user dictionary and replace with user id."""
    user_info: dict = tweet.pop("user")
    tweet["user_id_str"] = user_info["id_str"]
    return user_info


def remove_attributes(dictionary: dict, remove: List[str]) -> None:
    """Remove attributes from dictionary."""
    if type(dictionary) == dict:
        for column_name in remove:
            dictionary.pop(column_name, None)


def update_counts(tweet: dict) -> Tuple[dict, dict]:
    """return updated values of referenced tweet; with values:
    {status_id: (quote_count, reply_count, retweet_count and favorite_count)}
    """
    rt_count, qt_count = {}, {}  # set rt(retweet) and  qt(quoted tweet)

    if "retweeted_status" in tweet:
        rt = tweet["retweeted_status"]
        rt_c = rt["quote_count"], rt["reply_count"], rt["retweet_count"], rt["favorite_count"]
        rt_count = {rt["id_str"]: rt_c}
    if "quoted_status" in tweet:
        qt = tweet["quoted_status"]
        qt_c = qt["quote_count"], qt["reply_count"], qt["retweet_count"], qt["favorite_count"]
        qt_count = {qt["id_str"]: qt_c}

    return rt_count, qt_count


def extended_tweet_handler(tweet: dict) -> None:
    """Change the tweet with the full text, entities and text_range."""
    if "extended_tweet" in tweet:
        tweet["text"] = tweet["extended_tweet"]["full_text"]
        tweet["display_text_range"] = tweet["extended_tweet"]["display_text_range"]
        tweet["entities"] = tweet["extended_tweet"]["entities"]
        del tweet["extended_tweet"]

def coordinates_handler(tweet: dict) -> None:
    """Separates entities content (hashtags["text"] and user_mentions) into different columns."""
    if tweet["coordinates"]:
        tweet["latitude"] = tweet["coordinates"]["coordinates"][1]
        tweet["longitude"] = tweet["coordinates"]["coordinates"][0]

def entities_handler(tweet: dict) -> None:
    """Separates entities content (hashtags["text"] and user_mentions) into different columns."""
    tweet["hashtags"] = np.array([hashtag["text"] for hashtag in tweet["entities"]["hashtags"]])
    tweet["user_mentions"] = np.array([user_mention["id_str"] for user_mention in tweet["entities"]["user_mentions"]])

def cut_text(tweet: dict) -> None:
    """"""
    if "display_text_range" in tweet:
        begin, end = tweet["display_text_range"]
        tweet["text"] = tweet["text"][begin:end]

tweets, users, updated_counts = create_dictionaries(r"data\airlines-1558611772040.json")
tweets_df, users_df, updated_counts_df = create_dataframes(r"data\airlines-1558611772040.json")

print(tweets_df)
print("place count: ", tweets_df["place"].count())

# for filename in os.listdir("data"):
#     if filename.endswith(".json"):
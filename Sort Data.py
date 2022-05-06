import pandas as pd
import numpy as np
import json
import os
from typing import List, Dict, Set, Tuple
from remove_lists import *


def create_dataframes(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Creates 2 dataframes from given json file path: tweet and user."""
    tweets: List[dict] = []
    users: Dict[str, dict] = dict()

    with open(filepath, "r") as file:
        for line in file:
            tweet: dict = create_raw_tweet(line)

            if not tweet:  # continue if "Exceeded connection limit" error
                continue
            elif "delete" in tweet:  # continue if tweet is deleted
                continue
            elif "extended_tweet" in tweet:  # add full_text and such for extended tweets
                extended_tweet_handler(tweet)
            # !! TO DO: update favourite/retweet/reply counts before skipping retweet !!
#             elif "retweeted_status" in tweet:  # continue if it is a retweet
#                 continue

            user_info: dict = extract_user(tweet)

            remove_attributes(tweet, remove_tweet_attr)
            remove_attributes(user_info, remove_user_info_attr)
            remove_attributes(tweet["entities"], remove_tweet_entities_attr)

            for user_mention in tweet["entities"]["user_mentions"]:
                remove_attributes(user_mention, remove_user_mentions_attr)

            tweets.append(tweet)
            users[user_info.pop("id_str")] = user_info

    df_tweets = pd.DataFrame(tweets)
    df_users = pd.DataFrame.from_dict(users, orient='index')
    df_users.index.name = "user_id_str"
    return df_tweets, df_users


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
    for column_name in remove:
        dictionary.pop(column_name, None)

def extended_tweet_handler(tweet: dict) -> None:
    """Add the tweet with the full text, entities and text_range."""
    tweet["text"] = tweet["extended_tweet"]["full_text"]
    tweet["display_text_range"] = tweet["extended_tweet"]["display_text_range"]
    tweet["entities"] = tweet["extended_tweet"]["entities"]
    del tweet["extended_tweet"]


tweets_df, users_df = create_dataframes(r"data\airlines-1558611772040.json")
print(tweets_df)

# for filename in os.listdir("data"):
#     if filename.endswith(".json"):
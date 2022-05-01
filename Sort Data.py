import pandas as pd
import numpy as np
import json
import os
from typing import List, Dict, Set
from remove_lists import *

def create_dataframes(filepath: str) -> pd.DataFrame:
    """Create dataframe from given json file path."""
    tweets: List[dict] = []
    users: List[dict] = []

    with open(filepath, "r") as file:
        for line in file:

            tweet: dict = create_raw_tweet(line)
            if not tweet:  # continue if "Exceeded connection limit"
                continue
            elif "delete" in tweet:  # continue if tweet is deleted
                continue

            user_info: dict = extract_user(tweet)

            remove_attributes(tweet, remove_tweet)
            remove_attributes(user_info, remove_user_info)
            remove_attributes(tweet["entities"], remove_tweet_entities)

            for user_mention in tweet["entities"]["user_mentions"]:
                remove_attributes(user_mention, remove_user_mentions)

            tweets.append(tweet)
            users.append(user_info)

    tweets_df = pd.DataFrame(tweets)
    users_df = pd.DataFrame(users)
    return tweets_df, users_df

def create_raw_tweet(line: str) -> dict:
    """Create dictionary from json text line. Avoid the 'Exceeded connection limit' error.
    """
    try:
        tweet: dict = json.loads(line)
    except json.decoder.JSONDecodeError:
        tweet = None
        if line != "Exceeded connection limit for user\n":
            raise NameError(f'json loaderror with line: {line}')
    return tweet

def extract_user(tweet: dict) -> dict:
    """Extract user dictionary and replace with user id."""
    user_info: dict = tweet.pop("user")
    tweet["user_id_str"] = user_info["screen_name"]
    return user_info

def remove_attributes(dictionary: dict, remove: List[str]) -> None:
    """Remove attributes"""
    for columnname in remove:
        dictionary.pop(columnname, None)


tweets_df, users_df = create_dataframes(r"data\airlines-1558611772040.json")
print(tweets_df)
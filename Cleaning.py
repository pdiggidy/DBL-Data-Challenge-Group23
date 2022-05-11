import json
import numpy as np
from typing import List, Tuple, Dict


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
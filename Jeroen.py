import pandas as pd


def count_updater(original_df: pd.DataFrame, updated_values: pd.DataFrame) -> pd.DataFrame:
    """Docstring
    """

    try:  # for the first time when residu doesn't exist yet
        updated_values = updated_values.append(residu)
    except:
        True

    residu = pd.DataFrame()  # To reset it, since all current entries have been added to updated_values
    for id, row in updated_values.iterrows():  # here id is the tweet id, and row are the updated values
        id = str(id)
        if id in original_df.index:
            if original_df.loc[id, "quote_count"] < row["quote_count"]:   # Checks to make sure the highest
                original_df.loc[id, "quote_count"] = row["quote_count"]   # value is used.
            if original_df.loc[id, "reply_count"] < row["reply_count"]:
                original_df.loc[id, "reply_count"] = row["reply_count"]
            if original_df.loc[id, "retweet_count"] < row["retweet_count"]:
                original_df.loc[id, "retweet_count"] = row["retweet_count"]
            if original_df.loc[id, "favorite_count"] < row["favorite_count"]:
                original_df.loc[id, "favorite_count"] = row["favorite_count"]

        else:
            residu.loc[id, "quote_count"] = row["quote_count"]
            residu.loc[id, "reply_count"] = row["reply_count"]
            residu.loc[id, "retweet_count"] = row["retweet_count"]
            residu.loc[id, "favorite_count"] = row["favorite_count"]

    return original_df

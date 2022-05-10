import pandas as pd
from timeit import default_timer as timer


def count_updater(original_df: pd.DataFrame, updated_values: pd.DataFrame) -> pd.DataFrame:
    start = timer()
    original_df = original_df.set_index("id_str")
    for id, row in updated_values.iterrows():  # Where id is the tweet id, and row are the updated values
        id = str(id)
        if id in original_df.index:
            original_df.loc[id, "quote_count"] = row["quote_count"]
            original_df.loc[id, "reply_count"] = row["reply_count"]
            original_df.loc[id, "retweet_count"] = row["retweet_count"]
            original_df.loc[id, "favorite_count"] = row["favorite_count"]
    original_df = original_df.reset_index()
    print(timer() - start)
    return original_df

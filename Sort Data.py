import pandas as pd
import json
import os
from typing import List, Dict

def create_dataframe(filepath: str) -> pd.DataFrame:
    tweets = []
    with open(filepath, "r") as file:
        for line in file:
            try:
                tweet = json.loads(line)
            except json.decoder.JSONDecodeError:
                if line != "Exceeded connection limit for user\n":
                    print(line)
                    a = line
                    raise NameError(f"json loaderror with line: {line}")
            tweets.append(tweet)

    tweets_df = pd.DataFrame(tweets)
    return tweets_df
print(create_dataframe(r"data\airlines-1558611772040.json"))

def group_by_airline(tweets_df: pd.DataFrame):
    filenames: List[str] = os.listdir("data")
    readers: List[pd.DataFrame] = []

    for filename in filenames:
        file_path: str = os.path.join("data", filename)
        reader = create_dataframe(file_path)
        readers.extend(reader)
# all_dataframes("data")
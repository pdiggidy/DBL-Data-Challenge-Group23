import pandas as pd
import json
import os
from typing import List, Dict

# filenames: List[str] = os.listdir("data")
# readers: List[pd.DataFrame] = list()
# print(filenames)
# for filename in filenames:
#     dirname = os.path.join("data", filename)
#     print(dirname)
#     reader = pd.DataFrame(pd.read_json(dirname, lines=True))
#     readers.extend(reader)

# reader: pd.DataFrame = pd.read_json("data/airlines-1558611772040.json", lines=True)


def create_dataframe(filename: str):
    tweets = []
    with open(filename, "r") as file:
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
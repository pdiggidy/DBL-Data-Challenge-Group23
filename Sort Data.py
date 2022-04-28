import pandas as pd
import json

# from tabulate import tabulate

reader = pd.DataFrame(pd.read_json("Data/TestTweets_Repaired.json"))

for index in reader.index:
    if reader.iloc[index]['id'] != float(reader.iloc[index]['id_str']):
        print(reader.iloc[index])

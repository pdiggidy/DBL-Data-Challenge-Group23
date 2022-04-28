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

reader: pd.DataFrame = pd.DataFrame(pd.read_json("data/airlines-1558611772040.json", lines=True, orient="split"))

# reader = readers[0]
for index in reader.index:
    try:
        if int(reader.iloc[index]['id']) != int(reader.iloc[index]['id_str']):
                print(reader.iloc[index])
    except:
        print(reader.iloc[index])
# print(reader)
# print(os.listdir("data"))
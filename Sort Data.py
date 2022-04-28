import pandas as pd
import json
# from tabulate import tabulate

reader = pd.DataFrame(pd.read_json("Data/airlines-1558527599826.json", lines=True))
#print(tabulate(reader.head(), headers='keys'))
#for i in range(1,2):
#    print(reader.iloc[i])
for index in reader.index:
    if reader.iloc[index]['id'] != float(reader.iloc[index]['id_str']):
            print(reader.iloc[index])

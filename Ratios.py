import pandas as pd

df = pd.read_pickle("changes")
names = ["KLM", "AirFrance", "BritishAirways", "AmericanAir", "Lufthansa",
                 "EasyJet", "Ryanair", "SingaporeAir", "Qantas", "Ethihad", "VirginAtlantic"]
#df["company"] = df["company"].apply(lambda x: print(x))#lambda x: names[x])
df = df.groupby("company")
#changes = [df["change"].value_counts(normalize=True)[x] for x in range(0,(len(names)+1))]
# changes = []
# for name, group in df:
#     changes.append(group.value_counts(normalize=True))
print(df["change"].value_counts(normalize=True))
print("test")
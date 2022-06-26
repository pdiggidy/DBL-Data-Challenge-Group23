import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_pickle("changes")
names = ["KLM", "AirFrance", "BritishAirways", "AmericanAir", "Lufthansa", "AirBerlin",
                 "EasyJet", "Ryanair", "SingaporeAir", "Qantas", "Etihad", "VirginAtlantic"]
#df["company"] = df["company"].apply(lambda x: print(x))#lambda x: names[x])
df = df.groupby("company")
#changes = [df["change"].value_counts(normalize=True)[x] for x in range(0,(len(names)+1))]
# changes = []
# for name, group in df:
#     changes.append(group.value_counts(normalize=True))
#print(df["change"].value_counts(normalize=True))
changes_dict = {}
pos = []
neu = []
neg = []
for name, group in df:
    vals = group["change"].value_counts(normalize=True)
    ls = []
    for row in vals:
        ls.append(row)
    changes_dict[name] = ls
    pos.append(changes_dict[name][0])
    neu.append(changes_dict[name][1])
    neg.append(changes_dict[name][2])

print(np.add(np.add(pos,neu),neg))

#British Airways, Air France, EasyJet, Lufthansa, Ryanair, VirginAtlantic
names_with = ["British Airways", "Air France", "EasyJet", "Lufthansa", "Ryanair", "VirginAtlantic"]
names_without = ["KLM", "AmericanAir", "AirBerlin", "SingaporeAir", "Qantas", "Etihad"]
with_numbers = [2, 1, 6, 4, 7, 11]
without_numbers = [0, 3, 5, 8, 9, 10]

pos_with = [pos[i] for i in with_numbers]
pos_without = [pos[i] for i in without_numbers]
neu_with = [neu[i] for i in with_numbers]
neu_without = [neu[i] for i in without_numbers]
neg_with = [neg[i] for i in with_numbers]
neg_without = [neg[i] for i in without_numbers]

with_index = np.argsort(pos_with)
names_with = [names_with[i] for i in with_index]
without_index = np.argsort(pos_without)
names_without = [names_without[i] for i in without_index]

pos = [pos_with[i] for i in with_index] + [pos_without[i] for i in without_index]
neu = [neu_with[i] for i in with_index] + [neu_without[i] for i in without_index]
neg = [neg_with[i] for i in with_index] + [neg_without[i] for i in without_index]

names_sorted = names_with + names_without

fig, ax = plt.subplots()
ax.bar(names_sorted, pos, label="Positive", color = "g")
ax.bar(names_sorted, neu, label="Neutral", bottom = pos, color="orange")
ax.bar(names_sorted, neg, label="Negative", bottom = np.add(pos, neu), color= "r")
ax.set_xticklabels(names_sorted,rotation=45)
ax.legend()

plt.show()
print(np.add(np.add(pos,neu),neg))
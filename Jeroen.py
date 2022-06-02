import os
from sqlalchemy import create_engine
import pandas as pd
from CompanySort import *
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

# My personal testing file :)


connection = create_engine(os.environ["DB_STRING"]).connect()


def sent_received():
    df_a = pd.DataFrame()
    for i in range(len(company_names)):
        df_a.loc[i, "Name"] = company_names[i]
        df_a.loc[i, "id"] = str(company_id_list[i])

    for j in range(len(df_a)):
        df_airline = pd.read_sql_table(df_a.loc[j, "Name"], connection)
        sent = 0
        received = 0
        for tw in range(len(df_airline)):
            if str(df_airline.loc[tw, "user_id_str"]) == df_a.loc[j, "id"]:
                sent += 1
            else:
                received += 1
        df_a.loc[j, "sent"] = sent
        df_a.loc[j, "received"] = received
    return df_a


df_sent_receive = sent_received()
print(df_sent_receive)
fig = plt.figure(figsize=(16, 9))
ax = fig.add_axes([0, 0, 1, 1])

ax.bar(df_sent_receive["Name"], df_sent_receive["received"], width=0.8, color="b", label="Tweets received")
ax.bar(df_sent_receive["Name"], df_sent_receive["sent"], width=0.8, color="orange", alpha=0.8, label="Tweets sent")
plt.title("The amount of tweets sent and received per airline", size=16, weight="bold")
plt.xlabel("Airline")
plt.ylabel("Tweets")
plt.legend(["Tweets received", "Tweets sent"])
plt.savefig('image1.png', bbox_inches='tight')
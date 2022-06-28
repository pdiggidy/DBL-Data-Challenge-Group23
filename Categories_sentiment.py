from sqlalchemy import create_engine
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime
import re

air_lst = ["KLM", "BritishAirways","EasyJet", "Ryanair", "Average"]
           # "AmericanAir", "Lufthansa", "SingaporeAir", "VirginAtlantic"]
cats_regx_lst = ['(delay)', '(cancel)', '(bag)', '(service)', '(luggage)', '(food)', '(lunch)',
                 '(meal)', '(breakfast)', '(dinner)', '(boarding pass)', " (late)[ ,.?!]",
                 "(compensation)", "(refund)", "(check)-in|(check) in"]
cats_regx1: str = "|".join(cats_regx_lst)
cats_regx2: str = "(could|can |please|give|would).+(information)|no (information)"

cats_dict = {"bag": "Luggage issues", "luggage": "Luggage issues",
             "delay": "Delayed flights", "late": "Delayed flights",
             "cancel": "Cancelled flights",
             "service": "Customer service complaints",
             "food": "Food", "lunch": "Food", "meal": "Food", "breakfast": "Food", "dinner": "Food",
             "information": "Information request", "boarding pass": "Information request",
             "compensation": "Compensations/refunds", "refund": "Compensations/refunds",
             "check": "Check-in problems"}

query_text = """SELECT AT.airline, AT.timestamp_ms, AT.id_str, AT.text, C.sentiment_change
                FROM Conversations C
                INNER JOIN All_tweets AT
                ON C.tweet_id = AT.id_str
                WHERE C.msg_nr=1 AND AT.lang='en'
                """


def pick_month(month_number: int, text_df):
    text_df_copy = text_df.copy()
    text_df_copy.insert(1, "month", text_df.timestamp_ms.apply(lambda s: datetime.fromtimestamp(s/1000).month))
    text_df_copy = text_df_copy[text_df_copy["month"]==month_number].copy()
    return text_df_copy


def map_dict(text: str) -> set:
    """Return matching categories from a string
    """
    output1 = re.findall(cats_regx1, text.lower())
    output2 = re.findall(cats_regx2, text.lower())

    all_matches = set()
    for matches in (output1 + output2):
        matches_mapped = [cats_dict[match] for match in matches if match in cats_dict]
        all_matches.update(matches_mapped)

    ## additional conditions:
    if "Delayed flights" in all_matches and "Luggage issues" in all_matches:
        all_matches.remove("Delayed flights")
    if "Check-in problems" in all_matches and "Luggage issues" in all_matches:
        all_matches.remove("Luggage issues")

    return all_matches


def df_with_categories(text_df):
    """add a column with the categories in which the text falls. If the text belongs to no category, remove from table.
    """
    text_df["categories"] = text_df["text"].apply(map_dict)
    text_df.dropna(subset="categories", inplace=True)
    text_df.reset_index(drop=True, inplace=True)

    for column in cats_dict.values():
        text_df[column] = False
    for i in text_df.index:
        categs = text_df.loc[i, "categories"]
        for categ in categs:
            text_df.loc[i, categ] = True


def show_text_of_category(category, text_df):
    lst_i = []
    for index in text_df.index:
        if category in text_df.loc[index, "categories"]:
            lst_i.append(index)
    print(len(lst_i))
    return list(text_df.loc[lst_i,"text"])


def create_categories_df(airline_name, text_df):
    """Create a df for one airline which divides into subject categories and sentiment category.
    """
    if airline_name != "Average":
        air = text_df[text_df["airline"] == airline_name]
    elif airline_name == "Average":
        air = text_df
    catogs = set(cats_dict.values())
    catogs.remove("Information request")
    catogs.remove("Food")
    catogs.remove("Customer service complaints")  # reduce to 4
    catogs.remove("Delayed flights")  # reduce to 4

    cats_df = [
        air.loc[air[cat] == True, [cat, "sentiment_change"]].rename(columns={cat: "category"}).replace({True: cat})
        for cat in catogs]
    all_cat = pd.concat(cats_df, ignore_index=True)
    all_cat["sentiment_change"].replace({0: "neu", -1: "neg", 1: "pos"}, inplace=True)

    cat_sent_pivot_df = pd.crosstab(index=all_cat["category"], columns=all_cat["sentiment_change"], normalize="index")
    cat_sent_df = pd.melt(cat_sent_pivot_df.reset_index(), id_vars="category", value_vars=cat_sent_pivot_df.columns)
    cat_sent_df["airline"] = airline_name

    return cat_sent_df


def order_df_for_category(categ_name, df_all):
    df = df_all[df_all["category"] == categ_name].sort_values(["sentiment_change", "value"], ascending=False).copy()
    df1 = df[df["sentiment_change"] == "pos"]
    df2 = df[df["sentiment_change"] == "neu"]
    df3 = df[df["sentiment_change"] == "neg"]
    df_merge1 = df1.merge(df2, on="airline", how="left")
    df_merge2 = df_merge1.merge(df3, on="airline", how="left")

    dff1 = df_merge2.iloc[:,:3].copy()
    dff2 = df_merge2.iloc[:,4:7].copy()
    dff3 = df_merge2.iloc[:,7:10].copy()
    dff1.columns = ["category", "sentiment_change", 'value']
    dff2.columns = ["category", "sentiment_change", 'value']
    dff3.columns = ["category", "sentiment_change", 'value']
    df_all = pd.concat([dff3, dff2, dff1])
    df_all["airline"] = df_merge2["airline"].to_list() + df_merge2["airline"].to_list() + df_merge2["airline"].to_list()
    df_all["airline_n"] = df_all["airline"].replace({airl:i for i, airl in enumerate(df_all.airline.unique())})
    return df_all


def plot_categories(all_cat):
    cats_iter = all_cat["category"].unique()
    count = 0
    fig, ax_comb = plt.subplots(2, 2, figsize=(15, 9), sharex=True, sharey=False)
    fig.suptitle(f"Sentiment change of tweets per category for each airline", fontsize=30, fontweight=700)

    for ax_row in ax_comb:
        for ax in ax_row:
            if count == 6:
                break
            subject = cats_iter[count]
            subject_df = order_df_for_category(subject, all_cat).reset_index(drop=True)
            subject_df["value"] = subject_df["value"] * 100
            sns.histplot(subject_df,
                         y="airline", weights="value", hue="sentiment_change", discrete=True,
                         multiple="stack", shrink=0.7, palette=[(0.8, 0.0, 0.1), (1, 0.6, .0), (0.2, .7, 0.2)], ax=ax)
            ax.set_title(f"{subject}", fontweight=500, fontsize=26)
            ax.set_xlabel("Percentage", fontsize=18)
            ax.set_ylabel("")
            ax.legend("")
            count += 1
            ax.tick_params(labelsize=18)

    ax_comb[0, 1].legend(["Increase", "No change", "Decrease"], bbox_to_anchor=(1, 1), prop={"size": 18})
    # ax.yticks(fontsize=20)
    fig.tight_layout()
    plt.close(fig)

    for ax_row in ax_comb:
        for ax in ax_row:
            for ytick in ax.yaxis.get_major_ticks():
                ylabel_text = ytick.label
                ylabel_text.set_fontsize(18)
                if ylabel_text.get_text() == "KLM":
                    ylabel_text.set_fontweight(600)
                    ylabel_text.set_color((0.2, 0.4, 0.9))
    fig.tight_layout()

    fig_new = plt.figure()
    new_manager = fig_new.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)
    plt.show()
    plt.savefig("Categories_sentiment horizontal stacked bar plot")

    return fig, ax_comb


# ###### for whole dataset
# df_with_categories(text_df)
# hist_count_categories(text_df)
# all_cat = pd.concat([create_categories_df(name, text_df) for name in air_lst])
# fig, ax_comb = plot_categories(all_cat)


##### for month: uncomment and only change month_number variable##########
def plot_categories_sentiment(month_number):
    month_number = int(month_number)
    connection = create_engine(os.environ["DB_STRING"]).connect()
    text_df = pd.read_sql(query_text, connection)
    connection.close()

    text_month_df = pick_month(month_number, text_df)
    df_with_categories(text_month_df)
    month_cat = pd.concat([create_categories_df(name, text_month_df) for name in air_lst])
    plot_categories(month_cat)

plot_categories_sentiment(2)

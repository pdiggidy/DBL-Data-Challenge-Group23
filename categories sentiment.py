from sqlalchemy import create_engine
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime
import re

air_lst = ["KLM", "BritishAirways", "AmericanAir", "Lufthansa",
           "EasyJet", "Ryanair", "SingaporeAir", "VirginAtlantic"]

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
                FROM Conversations_2 C
                INNER JOIN All_tweets AT
                ON C.tweet_id = AT.id_str
                WHERE C.msg_nr=1 AND AT.lang='en'
                """

connection = create_engine(os.environ["DB_STRING"]).connect()
text_df = pd.read_sql(query_text, connection)
connection.close()


def pick_month(month_number: int, text_df):
    """Only select data of given month.
    """
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


def hist_count_categories(text_df):
    lst_all = [category for category_lst in text_df["categories"] for category in category_lst]
    fig_cat, ax_cat = plt.subplots(figsize=(20, 4))
    sns.histplot(lst_all, ax=ax_cat)
    plt.show()
    print("total count of categories:", len(lst_all))


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
    air = text_df[text_df["airline"] == airline_name]
    catogs = set(cats_dict.values())
    catogs.remove("Information request")
    catogs.remove("Food")
    catogs.remove("Customer service complaints")  # reduce to 4
    catogs.remove("Delayed flights")  # reduce to 4

    cats_df = [
        air.loc[air[cat] == True, [cat, "sentiment_change"]].rename(columns={cat: "category"}).replace({True: cat})
        for cat in catogs]
    all_cat = pd.concat(cats_df, ignore_index=True)
    all_cat["sentiment_change"].replace({-1: "very neg", -0.5: "neg", 0: "neu", 0.5: "pos", 1: "very pos"},
                                        inplace=True)

    cat_sent_pivot_df = pd.crosstab(index=all_cat["category"], columns=all_cat["sentiment_change"], normalize="index")
    cat_sent_df = pd.melt(cat_sent_pivot_df.reset_index(), id_vars="category", value_vars=cat_sent_pivot_df.columns)
    cat_sent_df["airline"] = airline_name

    return cat_sent_df


def order_df_for_category(categ_name, df_all):
    """Order the dataframe in the right position.
    """
    df = all_cat[all_cat["category"] == categ_name].sort_values(["sentiment_change", "value"], ascending=False).copy()
    df.set_index("airline", inplace=True)

    series_extend = df.value[df["sentiment_change"] == "very pos"] + df.value[df["sentiment_change"] == "pos"]
    df_extend = pd.DataFrame(series_extend)

    df_extend.insert(0, "sentiment_change", "pos_plus_pos")
    df_extend.insert(0, "category", categ_name)
    df_extend.sort_values("value", inplace=True, ascending=False)

    df1 = df[df["sentiment_change"] == "very pos"]
    df2 = df[df["sentiment_change"] == "pos"]
    df3 = df[df["sentiment_change"] == "neu"]
    df4 = df[df["sentiment_change"] == "neg"]
    df5 = df[df["sentiment_change"] == "very neg"]

    df_all_extend = pd.concat([df_extend, df1, df2, df3, df4, df5], axis=1)
    lst_dfs = [df_all_extend.iloc[:, 3 + 3 * i:6 + 3 * i] for i in range(5)]
    lst_dfs.reverse()
    df_all = pd.concat(lst_dfs)
    df_all.reset_index(inplace=True)
    return df_all


def plot_categories(all_cat):
    """Function to plot.
    """
    count = 0
    cats_iter = all_cat["category"].unique()
    fig, ax_comb = plt.subplots(2, 2, figsize=(15, 9), sharex=True, sharey=False)
    fig.suptitle(f"Sentiment change of tweets per category for each airline", fontsize=30, fontweight=700)

    for ax_row in ax_comb:
        for ax in ax_row:
            subject = cats_iter[count]
            count += 1
            subject_df = order_df_for_category(subject, all_cat).reset_index(drop=True)
            subject_df["value"] = subject_df["value"] * 100
            sns.histplot(subject_df,
                         y="airline", weights="value", hue="sentiment_change", discrete=True,
                         multiple="stack", shrink=0.7, ax=ax,
                         palette=[(0.7, 0.0, 0), (1, .3, 0.3), (1, 0.6, .0),(0.5, .9, 0.4), (0.1, .7, 0.1)])
            ax.set_title(f"{subject}", fontweight=500, fontsize=26)
            ax.set_xlabel("Percentage", fontsize=18)
            ax.set_ylabel("")
            ax.legend("").remove()
            ax.tick_params(labelsize=18)

    ax_comb[1, 0].legend(["Big increase", "Increase", "No change", "Decrease", "Big decrease"],
                         bbox_to_anchor=(-0.5, 0.6), prop={"size": 18})
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
    fig.tight_layout()
    plt.show()

    return fig, ax_comb


###### for whole dataset
df_with_categories(text_df)
hist_count_categories(text_df)
all_cat = pd.concat([create_categories_df(name, text_df) for name in air_lst])
fig, ax_comb = plot_categories(all_cat)


###### for month: uncomment and only change month_number variable##########
# month_number = 10
# text_month_df = pick_month(month_number, text_df)
# hist_count_categories(text_month_df)
# month_cat = pd.concat([create_categories_df(name, text_month_df) for name in air_lst])
# fig2, ax_comb2 = plot_categories(month_cat)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#df = pd.read_pickle("changes")
#names = ["KLM", "AirFrance", "BritishAirways", "AmericanAir", "Lufthansa", "AirBerlin",
#                 "EasyJet", "Ryanair", "SingaporeAir", "Qantas", "Etihad", "VirginAtlantic"]

def box_plots(df):
    df = df.groupby("company")

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


    ### Box Plots

    box = pd.DataFrame({"pos_with": np.multiply(pos_with,100), "pos_without": np.multiply(pos_without,100),
                        "neu_with": np.multiply(neu_with,100), "neu_without": np.multiply(neu_without,100),
                        "neg_with": np.multiply(neg_with,100), "neg_without": np.multiply(neg_without,100)})


    fig3, ax3 = plt.subplots(nrows=1, ncols=2, sharey=True,figsize=(10,7))
    ax3[0].boxplot(box[["pos_with", "pos_without"]], patch_artist=True,boxprops=dict(facecolor=(0.2, 0.7, 0.2)), medianprops=dict(color=(0.2,0.4,0.9), linewidth=2), widths=(0.5,0.5))
    ax3[1].boxplot(box[["neg_with", "neg_without"]], patch_artist=True, boxprops=dict(facecolor="orange"), medianprops=dict(color=(0.2,0.4,0.9), linewidth=2),widths=(0.5,0.5))
    ax3[0].set_xticklabels(["With\nNames", "Without\nNames"], size=20)
    ax3[1].set_xticklabels(["With\nNames", "Without\nNames"], size=20)
    ax3[0].tick_params(labelsize=18)
    ax3[1].tick_params(labelsize=18)
    ax3[0].set_title("Increase", size=20)
    ax3[1].set_title("Decrease", size=20)
    ax3[0].set_ylabel("Percentage", size=20)
    fig3.suptitle("Distribution of Sentiment Change", size=24)
    ax3[0].text( s="Virgin Atlantic",x=1, y=min(box["pos_with"]+1), size=12, ha="center")
    ax3[1].text( s="Virgin Atlantic",x=1, y=max(box["neg_with"]-2), size=12, ha="center")
    plt.tight_layout()
    plt.show()


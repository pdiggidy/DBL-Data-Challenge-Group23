from typing import List, Dict
import re

# WORK IN PROGRESS NOT READY TO USE

# KLM    56377143                   0
# AirFrance   106062176             1
# British_Airways   18332190        2
# AmericanAir   22536055            3
# Lufthansa   124476322             4
# AirBerlin   26223583              5
# AirBerlin assist   2182373406     6
# easyJet     38676903              7
# RyanAir    1542862735             8
# SingaporeAir   253340062          9
# Qantas     218730857              10
# EtihadAirways   45621423          11
# VirginAtlantic   20626359         12

company_id_list = [56377143, 106062176, 18332190, 22536055, 124476322, 26223583, 2182373406, 38676903, 1542862735,
                   253340062, 218730857, 45621423, 20626359]


def find_company(company_ids: List, tweet: Dict = None) -> List:
    # This code assumes we've already done the process of removing retweets and switching truncated text
    mentions = tweet["entities"]["user_mentions"]  # Extract the Mentions Section of the Tweet
    company = []  # the returned value is a list to account for the possibility that multiple companies mentioned

    if len(mentions) != 0:  # if there's no mentions then just skip
        for mention in mentions:
            user_id = int(mention["id_str"])
            if user_id in company_ids:
                # if the mentioned user id is in the list of id's, the index of that id is the number of the company
                company.append(company_ids.index(user_id))

    text = tweet["text"]  # if no companies are found in the mentions we need to look at the text
    if text is not None:  # We shouldn't get any None text because of the preprocessing, but just incase
        text = text.lower()
        if re.search(r" klm ", text) is not None:
            company.append(0)

    if len(company) != 0:  # Convert to the list to set and back to remove duplicates, and return it
        company = set(company)
        return list(company)
    else:
        return None
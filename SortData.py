from statistics import mean
import os
from Cleaning import *
from Conversations import *
from CompanySort import *
from Jeroen import * #for testing


def create_dictionaries(filepath: str) -> Tuple[List[dict], Dict[str, dict], Dict[str, tuple]]:
    """Creates 3 dictionaries from given json file path: tweets, users and updated_counts.
    """
    tweets: List[dict] = []
    users: Dict[str, dict] = dict()
    updated_counts: Dict[str, Tuple] = dict()

    with open(filepath, "r") as file:
        for line in file:
            # load the json file in a dictionary and handle errors
            tweet: dict = create_raw_tweet(line)

            # create dictionary with updated counts of quotes, replies, retweets and likes
            rt_count, qt_count = update_counts(tweet)

            # continue to next tweet if tweet is deleted or a retweet
            if ("delete" in tweet) or ("retweeted_status" in tweet):
                continue

            # for extended tweets: replace full_text,entities and text_range attributes
            extended_tweet_handler(tweet)

            # extract hashtags and user_mentions from entities and make separate columns of them
            entities_handler(tweet)
            # extract latitude and longitude from coordinates and make separate columns of them
            coordinates_handler(tweet)

            # only keep text within "display_text_range" bounds
            cut_text(tweet)

            # extract user dictionary and replace with user_id_str
            user_info: dict = extract_user(tweet)

            #Assign each tweet to one or more companies
            tweet["company"] = find_company(company_id_list, company_names, tweet)

            # remove abundant attributes from dictionaries
            remove_attributes(tweet, remove_tweet_attr)
            remove_attributes(user_info, remove_user_info_attr)
            remove_attributes(tweet["place"], remove_tweet_place_attr)

            # combine dictionaries of this tweet with other dictionaries
            tweets.append(tweet)
            users[user_info.pop("id_str")] = user_info
            updated_counts.update(rt_count)
            updated_counts.update(qt_count)

    return tweets, users, updated_counts


def create_dataframes(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Creates 3 dataframes from given json file path: tweets, users and updated_counts.
    """
    # create 3 collections of dictionaries
    tweets, users, updated_counts = create_dictionaries(filepath)

    # create 3 dataframes
    df_tweets = pd.DataFrame(tweets)

    df_users = pd.DataFrame.from_dict(users, orient='index')
    df_users.index.name = "user_id_str"

    updates_columns: list = ["quote_count", "reply_count", "retweet_count", "favorite_count"]
    df_updated_counts = pd.DataFrame.from_dict(updated_counts, columns=updates_columns, orient="index")

    df_tweets = df_tweets[df_tweets.company.notnull()]

    return df_tweets, df_users, df_updated_counts



# creating dataframes from json files
tweets, users, updated_counts = create_dictionaries("data/airlines-1558611772040.json")
tweets_df, users_df, updated_counts_df = create_dataframes("data/airlines-1558611772040.json")

# creating conversation dataframes
conversations = conversations_list_builder(tweets)
cleaned_conversations = conversations_cleaner(conversations)
conversations_df = conversations_list_to_df(cleaned_conversations)

# for debugging purposes
print(tweets_df)
test = count_updater(tweets_df, updated_counts_df)
print(test)

def decriptive_statistics():
    klm_tweets_df = tweets_df[tweets_df["user_id_str"] == str(klm_id)]
    bra_tweets_df = tweets_df[tweets_df["user_id_str"] == str(ba_id)]

    print(f"amount of loaded tweets after cleaning: \n{len(tweets_df)}\n"
          f"amount of loaded conversations: \n{len(conversations_df)}\n"
          f"amount of tweets per conversation within bound: \n"
          f"{min(len(conversation) for conversation in cleaned_conversations)} < amount < "
          f"{max(len(conversation) for conversation in cleaned_conversations)}\n"
          f"average amount of tweets per conversation: \n{mean(len(conversation) for conversation in cleaned_conversations)}\n"
          f"\n"
          f"amount of tweets send by KLM: \n{len(klm_tweets_df)}\n"
          f"amount of tweets send by British Airways: \n{len(bra_tweets_df)}\n"
          )


    decriptive_count = ["quote_count", "reply_count", "retweet_count", "favorite_count"]
    print("\nCumulative counts of quotes, replies, retweets and favorites of KLM and British Airways:\n",
        pd.DataFrame({"KLM": dict((count, sum(klm_tweets_df[count])) for count in decriptive_count),
                      "British Airways": dict((count, sum(bra_tweets_df[count])) for count in decriptive_count)}
                     )
    )
    print("\nAverage counts of quotes, replies, retweets and favorites of KLM and British Airways per 100 tweets:\n",
        pd.DataFrame({"KLM": dict( ( count, sum(klm_tweets_df[count]) / len(klm_tweets_df) )
                                  for count in decriptive_count),
                      "British Airways": dict( ( count, sum(bra_tweets_df[count]) / len(bra_tweets_df) )
                                  for count in decriptive_count)}
                     )
          )

decriptive_statistics()

# def run_data_directory():
#     """Run with all data in 'data' directories"""
#     tweets_dfs, users_dfs, updated_counts_dfs = [], [], []
#     for filename in os.listdir("data"):
#         path_name = os.path.join("data", filename)
#         tweets_frame, users_frame, updated_counts_frame = create_dataframes(path_name)
#         tweets_dfs.append(tweets_frame)
#         users_dfs.append(users_frame)
#         updated_counts_dfs.append(updated_counts_frame)
#     return tweets_dfs, users_dfs, updated_counts_dfs
# print([len(df) for dfs in run_data_directory() for df in dfs])

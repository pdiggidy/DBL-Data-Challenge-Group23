def snelle_jelle(twt_list):
    """Snel ff."""
    count = 0
    for tweet in twt_list:
        if tweet['in_reply_to_status_id_str'] is None and tweet['in_reply_to_user_id_str'] is not None:
            print(tweet['id_str'])
            count += 1
    print(count)
snelle_jelle(tweets)


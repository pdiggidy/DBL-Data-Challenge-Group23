remove_tweet_attr: list = ['created_at', 'id', 'display_text_range', 'source', 'truncated', 'in_reply_to_status_id',
                           'in_reply_to_user_id', 'in_reply_to_screen_name', 'geo', 'coordinates',
                           'contributors', 'entities', 'is_quote_status', 'extended_entities', 'favorited', 'retweeted',
                           'possibly_sensitive', 'filter_level', 'quoted_status_id',
                           'quoted_status', 'quoted_status_permalink']
remove_user_info_attr: list = ['id', 'name', 'screen_name', 'location', 'url', 'description', 'translator_type',
                               'protected', 'friends_count', 'listed_count',
                               'favourites_count', 'statuses_count', 'created_at',
                               'utc_offset', 'time_zone', 'geo_enabled', 'lang',
                               'contributors_enabled', 'is_translator',
                               'profile_background_color', 'profile_background_image_url',
                               'profile_background_image_url_https', 'profile_background_tile',
                               'profile_link_color', 'profile_sidebar_border_color',
                               'profile_sidebar_fill_color', 'profile_text_color',
                               'profile_use_background_image', 'profile_image_url',
                               'profile_image_url_https', 'profile_banner_url',
                               'default_profile', 'default_profile_image', 'following',
                               'follow_request_sent', 'notifications']
remove_hashtags_attr: list = ['indices']
remove_tweet_place_attr: list = ['id', 'url']  # unfinished

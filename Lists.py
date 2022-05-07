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

airlines_list: list = [56377143,  # KLM
                       106062176, 18332190, 22536055,          # AirFrance, BritishAirways, AmericanAir,
                       124476322, 26223583, 2182373406,        # Lufthansa, AirBerlin, AirBerlin Assist,
                       38676903, 1542862735, 253340062,        # easyJet, RyanAir, SingaporeAir
                       218730857, 45621423, 20626359]          # Qantas, EtihadAirways, VirginAtlantic
klm_id: int = 56377143
ba_id: int = 18332190
airlines_list_wo_klm: list = [106062176,   # AirFrance
                              18332190,    # BritishAirways
                              22536055,    # AmericanAir
                              124476322,   # Lufthansa
                              26223583,    # AirBerlin
                              2182373406,  # AirBerlin Assist
                              38676903,    # easyJet
                              1542862735,  # RyanAir
                              253340062,   # SingaporeAir
                              218730857,   # Qantas
                              45621423,    # EtihadAirways
                              20626359]    # VirginAtlantic

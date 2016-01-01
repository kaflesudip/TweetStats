from twython import Twython
from models import Tweet

import datetime
import traceback
# import time

# first
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


# second
APP_KEY2 = ''
APP_SECRET2 = ''
OAUTH_TOKEN2 = ''
OAUTH_TOKEN_SECRET2 = ''


# third
APP_KEY3 = ''
APP_SECRET3 = ''
OAUTH_TOKEN3 = ''
OAUTH_TOKEN_SECRET3 = ''


def rotate_key():
    global APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
    global APP_KEY2, APP_SECRET2, OAUTH_TOKEN2, OAUTH_TOKEN_SECRET2
    global APP_KEY3, APP_SECRET3, OAUTH_TOKEN3, OAUTH_TOKEN_SECRET3

    APP_KEY, APP_KEY2, APP_KEY3 = APP_KEY3, APP_KEY, APP_KEY2
    APP_SECRET, APP_SECRET2, APP_SECRET3 = APP_SECRET3, APP_SECRET, APP_SECRET2
    OAUTH_TOKEN, OAUTH_TOKEN2, OAUTH_TOKEN3 = OAUTH_TOKEN3, OAUTH_TOKEN, OAUTH_TOKEN2
    OAUTH_TOKEN_SECRET, OAUTH_TOKEN_SECRET2, OAUTH_TOKEN_SECRET3 =\
        OAUTH_TOKEN_SECRET3, OAUTH_TOKEN_SECRET, OAUTH_TOKEN_SECRET2


def update_given_tweet(tweet_id):

    twitter = Twython(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        oauth_token=OAUTH_TOKEN,
        oauth_token_secret=OAUTH_TOKEN_SECRET,
    )
    try:
        status = twitter.show_status(id=tweet_id)
        return status
    except Exception as err:
        # rotate_key()
        print(err.msg)
        if 'rate limit exceeded' in err.msg.lower() or 'max retries' in err.msg.lower():
            rotate_key()
            # twitter = Twython(
            #     app_key=APP_KEY,
            #     app_secret=APP_SECRET,
            #     oauth_token=OAUTH_TOKEN,
            #     oauth_token_secret=OAUTH_TOKEN_SECRET,
            # )
            traceback.print_tb(err.__traceback__)
            return update_given_tweet(tweet_id)
        traceback.print_tb(err.__traceback__)
        return False


def update_database():
    print("fetching")
    tweets = Tweet.objects(total_fetched=1, error_occured__ne=True)
    print("updating")
    i = 0
    error_count = 0
    for each_tweet in tweets:
        print("loop")
        data = update_given_tweet(each_tweet.tweet_id)
        if not data:
            error_count += 1
            print("!!!!!!!!!error", error_count, "correct", i)
            each_tweet.error_occured = True
            each_tweet.save()
            continue
        elif data == 3:
            continue
        print("got data")
        data['fetched_timestamp'] = datetime.datetime.now()
        data['fresh_tweet'] = False
        data['update_count'] = 2
        each_tweet.total_fetched = 2
        each_tweet.tweets.append(data)
        each_tweet.save()
        print(i, "errors=", error_count)
        i += 1

update_database()

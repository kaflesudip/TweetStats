#!/usr/bin/env python
# encoding: utf-8
from twython import Twython, TwythonStreamer
from models import Tweet
import datetime

APP_KEY = '9KcrkaDo5VU7ZXvePydFaavU1'
APP_SECRET = 'wusZhyHMVg86GYuq86q8i5QdpJqyxgJb1cVf2PIKSHf0J33vWY'
OAUTH_TOKEN = '137592952-UbPQLHixGEPa8PixO7tuwvxWPJ7osRjHSz8tyeJj'
OAUTH_TOKEN_SECRET = 'AxZunGLLwQa3pN8rVqLSSpPolYt69JGuSI6JazEZZmtpI'


class OauthToken():
    APP_KEY = '9KcrkaDo5VU7ZXvePydFaavU1'
    APP_SECRET = 'wusZhyHMVg86GYuq86q8i5QdpJqyxgJb1cVf2PIKSHf0J33vWY'

    def get_token(self):
        twitter = Twython(self.APP_KEY, self.APP_SECRET)
        auth = twitter.get_authentication_tokens('http://localhost:8000/')
        return auth


class MyStreamer(TwythonStreamer):

    i = 0

    def on_success(self, data):
        if 'text' in data:
            data['fetched_timestamp'] = datetime.datetime.now()
            data['fresh_tweet'] = True
            tweet = Tweet()
            tweet.tweet_id = data['id_str']
            tweet.tweets.append(data)
            tweet.save()
            print("saved", self.i)
            self.i += 1

    def on_error(self, status_code, data):
        print("error")

'''
obtain tweet from sample post and save the tweet posts in the database
'''
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

while True:
    try:
        stream.statuses.sample()
    except:
        print("!!!!!!!!! error !!!!!!!!!!!!1")

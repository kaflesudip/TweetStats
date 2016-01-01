from mongoengine import DynamicDocument, fields, connect

connect('tweetpredict')


class Tweet(DynamicDocument):
    tweet_id = fields.StringField()
    tweets = fields.ListField()
    total_fetched = fields.IntField()
    error_occured = fields.BooleanField()

# TweetStats
Collect tweet and see their stats after 1, 2 and 3 days.

## How?
1. Install requirements at first. `pip install -r requirements.txt`
2. Install Mongodb on your computer.
3. Add API keys from twitter to `get_tweets.py` and `update_tweets.py`
4. Run `python get_tweets.py`.
5. Add `update_tweets.py` to cronjob or use celery to periodically run the update.


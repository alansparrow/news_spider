from spider import Spider
from peewee import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import hashlib
import time
from news_model import *
from datetime import datetime
import tweepy
import json
from news_model import *
import logging

class TwitterSpider(Spider):
    auth = tweepy.OAuthHandler('kfyMTB7TeS8VGPmROxJeE1z7U', 'lYM2kiFX8HQtRB6zyVusexNH8q8Jb652Kd4fxdWAdB3kUtbGo4')
    auth.set_access_token('908220700644667393-Vll7KNpLjrwsPzz3FndoqU5GBHDulxi', 'UqOJjLFG5tj49SleIJp7aOg13XV0Adqk79cP3ibtsKbaO')

    api = tweepy.API(auth)

    def __init__(self):
        self.following_list = [
                            # 'aantonop',
                            # 'petertoddbtc',
                            'VitalikButerin'
                            # 'SatoshiLite',
                            # 'ethereumproject'
                        ]

    def __str__(self):
        return '\n'.join(self.following_list)

    def check_and_update_database(self, tweet_news):

        try:
            saved_news = News.select().where(News.fingerprint == tweet_news.fingerprint).get()
        except News.DoesNotExist:
            saved_news = None

        if (saved_news == None):
            tweet_news.save()
            self.send_notification(tweet_news)
            print(tweet_news.title + "    " + tweet_news.url + "   " + tweet_news.fingerprint)

    def roam(self):
        new_news = News(
                                title = '',
                                url = '',
                                pub_date = '', 
                                pub_source = '',
                                fingerprint = ''
                            )
        try:
            for user in self.following_list:
                tweets = tweepy.Cursor(self.api.user_timeline, id=user).items(20)
                
                for tweet in tweets:
                    tweet_url = 'https://twitter.com/' + user + '/status/' + tweet.id_str
                    new_news = News(
                                title = tweet.text,
                                url = tweet_url,
                                # pub_date = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y"),
                                pub_date = tweet.created_at,
                                pub_source = 'https://twitter.com/' + user,
                                fingerprint = hashlib.sha256(tweet_url.encode()).hexdigest()
                            )
                    # print(new_news.title)
                    if (hasattr(tweet, 'retweeted_status') and 
                            self.check_related_content(tweet.text)):   # retweet
                        self.check_and_update_database(new_news)
                    else:
                        if (tweet.in_reply_to_screen_name == None and
                                self.check_related_content(tweet.text)):   # self tweet
                            self.check_and_update_database(new_news)
                        else:
                            pass
        except Exception as e:
            print(new_news.url + "   " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            logging.exception(e)
# ts = TwitterSpider()
# ts.roam()
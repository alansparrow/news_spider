from spider import Spider
from peewee import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import hashlib
import time
from news_model import *
from datetime import datetime
import logging
import random

SCORE_GRAVITY = 1.8

def cal_score(news):
    if (news == None):
        return 0.0

    up_down_diff = news.up_vote_count - news.down_vote_count
    time_diff = (datetime.utcnow() - news.pub_date.replace(tzinfo=None)).total_seconds() / 3600
    score = 0.0
    noise = random.uniform(0.1, 0.2)
    if (up_down_diff - 1 > 0):
        score = (up_down_diff - 1) / ((time_diff + 2) ** SCORE_GRAVITY)
    else:
        score = (up_down_diff - 1) * ((time_diff + 2) ** SCORE_GRAVITY)

    score += noise

    return score

news_list = News.select()
for news in news_list:
    news.up_vote_count = random.randint(0, 1000)
    news.down_vote_count = random.randint(0, 1000)
    news.score = cal_score(news)
    print(str(news.id) + ":   " + str(news.score))
    news.save()
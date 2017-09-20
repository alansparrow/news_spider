# -*- coding: utf-8 -*-

from peewee import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import hashlib
import time
from news_model import *
from datetime import datetime
from fcm import FCM
import re

class Spider:
    sensitive_simple_words = ['ico', 'icos', 'bitcoin', 'ethereum', 'litecoin',
                     'cryptocurrency', 'cryptocurrencies', 'crypto-currency',
                       'token', 'tokens', 'blockchain', 'blockchains', 'fud',
                       '$btc', '$eth', '$ltc', 'btc', 'eth', 'ltc']

    sensitive_complex_words = ['crypto currency', 'crypto currencies']

    psql_db = PostgresqlDatabase('news_spider', user='baotrungtn')

    def __init__(self):
        pass

    def send_notification(self, news):
        status_code = FCM(news).send_notification()
        print("Sent notification: " + str(status_code))

    def check_related_content(self, title):
        title = title.strip().lower()
        for s_word in Spider.sensitive_simple_words:
            for t_word in title.split():
                t_word_clean = re.sub('[^A-Za-z0-9]+', '', t_word)
                if (s_word == t_word_clean):
                    return True

        for s_word in Spider.sensitive_complex_words:
            if (title.find(s_word) != -1):
                return True

        return False

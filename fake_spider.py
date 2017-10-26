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

class FakeSpider(Spider):
    def __init__(self):
        pass

    def roam(self):
        new_news = News(
                                title = 'Fake News ' + str(random.randint(0,1000)),
                                url = 'http://google.com',
                                pub_date = datetime.utcnow(), 
                                pub_source = 'http://google.com',
                                fingerprint = hashlib.sha256("fake text".encode()).hexdigest()
                            )
        try:
            new_news.save()
            self.send_notification(new_news)
            print(new_news.title + "    " + new_news.url + "   " + new_news.fingerprint)
        except Exception as e:
            logging.exception(e)
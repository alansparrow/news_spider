from spider import Spider
from peewee import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import hashlib
import time
from news_model import *
from datetime import datetime
import logging

class HNSpider(Spider):
    def __init__(self):
        self.url_list = [
                            'https://news.ycombinator.com',
                            'https://news.ycombinator.com/news?p=2',
                            'https://news.ycombinator.com/news?p=3',
                            'https://news.ycombinator.com/newest'
                        ]

    def __str__(self):
        return '\n'.join(self.url_list)

    def roam(self):
        new_news = News(
                                title = '',
                                url = '',
                                pub_date = '', 
                                pub_source = '',
                                fingerprint = ''
                            )
        try:
            for url in self.url_list:
                # query the website and return the html to the variable ‘page’
                page = urlopen(url)    

                # parse the html using beautiful soap and store in variable `soup`
                soup = BeautifulSoup(page, 'html.parser')

                for EachPart in soup.find_all('a'):
                    news_original_text = EachPart.get_text().strip()
                    
                    news_text = news_original_text.lower()
                        
                    if self.check_related_content(news_text):
                        fingerprint = hashlib.sha256(news_text.encode()).hexdigest()
                        try:
                            saved_news = News.select().where(News.fingerprint == fingerprint).get()
                        except News.DoesNotExist:
                            saved_news = None

                        if (saved_news == None):
                            new_news = News(
                                title = news_original_text[:255],
                                url = EachPart.get('href'),
                                pub_date = datetime.now(), 
                                pub_source = url,
                                fingerprint = fingerprint
                            )

                            # Only for Hackernews
                            # Pass

                            try:
                                saved_news = News.select().where(News.url == new_news.url).get()
                            except News.DoesNotExist:
                                saved_news = None

                            if (saved_news == None):
                                new_news.save()
                                self.send_notification(new_news)
                                print(new_news.title + "    " + new_news.url + "   " + fingerprint)
        except Exception as e:
            print(new_news.url + "   " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            logging.exception(e)
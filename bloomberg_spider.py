from spider import Spider
from peewee import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import hashlib
import time
from news_model import *
from datetime import datetime
import logging


class BloombergSpider(Spider):
    def __init__(self):
        self.url_list = [
                            'https://www.bloomberg.com',
                            'https://www.bloomberg.com/technology',
                            'https://www.bloomberg.com/politics',
                            'https://www.bloomberg.com/markets',
                            'https://www.bloomberg.com/pursuits',
                            'https://www.bloomberg.com/businessweek',
                            'https://www.bloomberg.com/asia'
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
                                title = news_original_text,
                                url = EachPart.get('href'),
                                pub_date = datetime.now(), 
                                pub_source = url,
                                fingerprint = fingerprint
                            )

                            # Only for Bloomberg
                            if (new_news.url.find('https://www.bloomberg.com') == -1):
                                new_news.url = 'https://www.bloomberg.com' + new_news.url
                            p = urlopen(new_news.url)
                            s = BeautifulSoup(p, 'html.parser')
                            t = s.find_all('time', {'class': 'article-timestamp'})
                            
                            
                            if (len(t) != 0):
                                t = t[0].attrs['datetime']
                                utc_dt = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
                            else: # video
                                t = s.find_all('time', {'class': 'published-at'})
                                if (len(t) != 0):
                                    t = t[0].attrs['datetime']
                                    utc_dt = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
                                else:
                                    utc_dt = datetime.now()
                                                            
                            new_news.pub_date = utc_dt
                            
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

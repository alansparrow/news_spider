# -*- coding: utf-8 -*-

from peewee import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import hashlib
import time
from news_model import *
from datetime import datetime

sensitive_words = ['ico', 'icos', 'bitcoin', 'ethereum',
                     'cryptocurrency', 'cryptocurrencies',
                      'crypto currency', 'crypto currencies',
                       'token', 'tokens']
psql_db = PostgresqlDatabase('news_spider', user='baotrungtn')

quote_pages = ['https://www.bloomberg.com/technology',
                'https://news.ycombinator.com/',
                'https://www.technologyreview.com/'
                ]

def check_related_content(title, sensitive_words):
    for s_word in sensitive_words:
        for t_word in title.split():
            if (s_word == t_word):
                return True
    return False

while True:
        
    for quote_page in quote_pages:
        # query the website and return the html to the variable ‘page’
        page = urlopen(quote_page)    

        # parse the html using beautiful soap and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')

        for EachPart in soup.find_all('a'):
            news_original_text = EachPart.get_text().strip()
            news_text = news_original_text.lower()
            if check_related_content(news_text, sensitive_words):
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
                        pub_source = quote_page,
                        fingerprint = fingerprint
                    )

                    if (quote_page == 'https://www.bloomberg.com/technology'):
                        """learn more about scope """
                        
                        new_news.url = 'https://www.bloomberg.com' + new_news.url
                        p = urlopen(new_news.url)
                        s = BeautifulSoup(p, 'html.parser')
                        t = s.find_all('time', {'class': 'article-timestamp'})[0].attrs['datetime']
                        utc_dt = datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
                        new_news.pub_date = utc_dt
                    
                    try:
                        saved_news = News.select().where(News.url == new_news.url).get()
                    except News.DoesNotExist:
                        saved_news = None

                    if (saved_news == None):
                        new_news.save()
                        print(news_text + "    " + EachPart.get('href') + "   " + fingerprint)
    print("Reload... at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(10)



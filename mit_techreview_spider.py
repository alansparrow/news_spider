from spider import Spider
from peewee import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import hashlib
import time
from news_model import *
from datetime import datetime
import logging

class MITTechReviewSpider(Spider):
    def __init__(self):
        self.url_list = [
                            'https://www.technologyreview.com/'
                        ]

    def __str__(self):
        return '\n'.join(self.url_list)

    def refine_date(self, str):        
        str = str.replace('January', '1')
        str = str.replace('February', '2')
        str = str.replace('March', '3')
        str = str.replace('April', '4')
        str = str.replace('May', '5')
        str = str.replace('June', '6')
        str = str.replace('July', '7')
        str = str.replace('August', '8')
        str = str.replace('September', '9')
        str = str.replace('October', '10')
        str = str.replace('November', '11')
        str = str.replace('December', '12')
        str = str.replace(',', '').strip()
        return str

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
                        except Exception, e:
                            print(e.pgerror)
                            saved_news = None

                        if (saved_news == None):
                            new_news = News(
                                title = news_original_text,
                                url = EachPart.get('href'),
                                pub_date = datetime.now(), 
                                pub_source = url,
                                fingerprint = fingerprint
                            )

                            # Only for MITTechReview
                            new_news.url = 'https://www.technologyreview.com' + new_news.url
                            p = urlopen(new_news.url)
                            s = BeautifulSoup(p, 'html.parser')
                            

                            
                            t = s.find_all('li', {'class': 'article-topper__meta-item'})
                            try:
                                if (len(t) > 0):
                                    t = self.refine_date(t[1].get_text())
                                elif (len(t) == 0):  # video
                                    t = s.find_all('p', {'class': 'primary-video__pubdate'})
                                    t = self.refine_date(t[0].get_text())
                                    video_title = s.find_all('h1', {'class': 'primary-video__title'})[0].get_text().strip()
                                    new_news.title = video_title
                            except IndexError:
                                continue
                            
                            utc_dt = datetime.strptime(t, "%m %d %Y")
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

# t = MITTechReviewSpider()
# t.roam()
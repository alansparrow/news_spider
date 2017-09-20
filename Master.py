import time
from datetime import datetime
from hn_spider import HNSpider
from bloomberg_spider import BloombergSpider
from mit_techreview_spider import MITTechReviewSpider
from twitter_spider import TwitterSpider
import logging

hn_spider = HNSpider()
bb_spider = BloombergSpider()
mit_spider = MITTechReviewSpider()
twitter_spider = TwitterSpider()

while True:
    
    try:
        while True:
            hn_spider.roam()
            bb_spider.roam()
            mit_spider.roam()
            twitter_spider.roam()
            time.sleep(60)
            print("Reload... " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    except Exception as e:
        logging.exception(e)

    time.sleep(60)
    print('Restarting due to error... ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



import time
from datetime import datetime
from HNSpider import HNSpider
from BloombergSpider import BloombergSpider
from MITTechReviewSpider import MITTechReviewSpider
from TwitterSpider import TwitterSpider
import logging

hn_spider = HNSpider()
bb_spider = BloombergSpider()
mit_spider = MITTechReviewSpider()
twitter_spier = TwitterSpider()

while True:
    
    try:
        while True:
            hn_spider.roam()
            bb_spider.roam()
            mit_spider.roam()
            twitter_spier.roam()
            time.sleep(60)
            print("Reload... " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    except Exception as e:
        logging.exception(e)

    time.sleep(60)
    print('Restarting due to error... ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



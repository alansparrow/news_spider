import time
from datetime import datetime
from hn_spider import HNSpider
from bloomberg_spider import BloombergSpider
from mit_techreview_spider import MITTechReviewSpider
from twitter_spider import TwitterSpider
import logging

print("Hello! I am Spider. I will start collecting news...")

while True:
    
    try:
        while True:
            HNSpider().roam()
            BloombergSpider().roam()
            MITTechReviewSpider().roam()
            # TwitterSpider().roam()
            time.sleep(60)
            print("Reload... " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    except Exception as e:
        logging.exception(e)

    time.sleep(60)
    print('Restarting due to error... ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



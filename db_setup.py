from peewee import *
from news_model import *
import datetime

psql_db = PostgresqlDatabase('news_spider', user='baotrungtn')

psql_db.connect()
psql_db.create_tables([News])

# n = News(title='abc', url='aaa', pub_date=datetime.datetime.now(), pub_source='aaa', fingerprint='1111')
# n.save()
# try:
#     n = News.select().where(News.fingerprint == '1111').get()
# except News.DoesNotExist:
#     n = None

# print(n)
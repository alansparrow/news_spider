from peewee import *
from datetime import datetime
import random
psql_db = PostgresqlDatabase('news_spider', user='baotrungtn', password='baotrung', host='192.241.147.78', port='5432')

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class News(BaseModel):
    created_date = DateTimeField(default=datetime.utcnow())
    modified_date = DateTimeField(default=datetime.utcnow())

    title = TextField()
    url = TextField()
    pub_date = DateTimeField()
    pub_source = TextField()
    fingerprint = TextField()
    buy_vote_count = IntegerField(default=0)
    sell_vote_count = IntegerField(default=0)
    hold_vote_count = IntegerField(default=0)
    fact_vote_count = IntegerField(default=0)
    opinion_vote_count = IntegerField(default=0)
    up_vote_count = IntegerField(default=0)
    down_vote_count = IntegerField(default=0)
    score = FloatField(default=random.uniform(0.1, 0.2))

    def __str__(self):
        return self.title

from peewee import *
psql_db = PostgresqlDatabase('news_spider', user='baotrungtn')

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class News(BaseModel):
    title = CharField()
    url = CharField()
    pub_date = DateTimeField()
    pub_source = CharField()
    fingerprint = CharField()
    buy_vote_count = IntegerField(default=0)
    sell_vote_count = IntegerField(default=0)
    hold_vote_count = IntegerField(default=0)

    def __str__(self):
        return self.title

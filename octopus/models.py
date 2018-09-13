from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField
from .config import DB_HOST


db = SqliteDatabase(DB_HOST)


class BaseModel(Model):
    class Meta:
        database = db


class URL(BaseModel):
    hash = CharField(unique=True, primary_key=True)
    value = CharField(unique=True)
    sentiment = IntegerField(null=True)


class Token(BaseModel):
    hash = CharField(unique=True, primary_key=True)
    value = CharField(unique=True)
    frequency = IntegerField(null=True)

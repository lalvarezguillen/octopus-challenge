from typing import Optional, List, Iterator
from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField
from .config import DB_HOST
from .crypto import salted_hash, encrypt, decrypt
from .nlp import TokenCount
from .schemas import TokenSchema


db = SqliteDatabase(DB_HOST)


class BaseModel(Model):
    class Meta:
        database = db


class URL(BaseModel):
    hash = CharField(primary_key=True)
    value = CharField(unique=True)
    sentiment = IntegerField(default=0)

    @classmethod
    def get_by_hash(cls, url: str) -> Optional["URL"]:
        try:
            return cls.get(hash=salted_hash(url))
        except cls.DoesNotExist:
            return None

    @classmethod
    def new(cls, url: str) -> "URL":
        return cls.create(hash=salted_hash(url), value=url)


class Token(BaseModel):
    hash = CharField(primary_key=True)
    encrypted = CharField(unique=True)
    frequency = IntegerField(default=0)

    @classmethod
    def batch_update(cls, counts: List[TokenCount]) -> List["Token"]:
        return list(map(cls.update_count, counts))

    @classmethod
    def update_count(cls, count: TokenCount) -> "Token":
        token_hash = salted_hash(count["token"])
        try:
            token = cls.get(hash=token_hash)
        except cls.DoesNotExist:
            token = cls.create(
                hash=token_hash, encrypted=encrypt(count["token"])
            )
        token.frequency += count["frequency"]
        token.save()
        return token

    @classmethod
    def get_page(cls, page: int, size: int) -> List[TokenCount]:
        print(page, size)
        cursor = (
            cls.select()
            .order_by(cls.frequency.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        return [cls.decrypt_entry(entry) for entry in cursor]

    @staticmethod
    def decrypt_entry(entry: "Token") -> TokenCount:
        entry.encrypted = decrypt(entry.encrypted)
        return TokenSchema().dump(entry).data


db.connect()
db.create_tables([URL, Token])

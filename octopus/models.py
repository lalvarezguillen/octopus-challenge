"""
This module should contain the code required to interact
with our DB.
"""
from typing import Optional, List, Iterator, Tuple
from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField
from .crypto import Encryptor
from .nlp import TokenCount
from .schemas import TokenSchema

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class URL(BaseModel):
    """ 
    Represents URLs we have visited
    """

    hash = CharField(primary_key=True)
    value = CharField(unique=True)
    sentiment = IntegerField(default=0)

    @classmethod
    def get_by_hash(cls, url: str, enc: Encryptor) -> Optional["URL"]:
        """
        Fetches the DB entry of a URL, if it exists.
        Args:
            url: The plain URL whose entry we want to fecth
            enc: an object that's capable of hashing the URL
        Returns:
            The DB entry of the URL, if it exists.
        """
        try:
            return cls.get(hash=enc.salted_hash(url))
        except cls.DoesNotExist:
            return None

    @classmethod
    def new(cls, url: str, enc: Encryptor) -> "URL":
        """
        Creates a new DB entry for a URL.
        Args:
            url: The plain text version of the URL.
            enc: an object that's capable to hashing the URL.
        Returns:
            The newly created DB entry.
        """
        return cls.create(hash=enc.salted_hash(url), value=url)


class Token(BaseModel):
    """
    Represents non-stopwords words encountered in pages visited.
    """

    hash = CharField(primary_key=True)
    encrypted = CharField(unique=True)
    frequency = IntegerField(default=0)

    @classmethod
    def batch_update(
        cls, counts: List[TokenCount], enc: Encryptor
    ) -> List["Token"]:
        """
        Increases the frequency counts of a collection of tokens.
        Args:
            counts: A collection of tokens with their frequencies.
            enc: An object capable of encrypting and hashing token
        Returns:
            A list of the DB entries of the newly updated/created tokens
        """
        return list(map(lambda x: cls.update_count(x, enc), counts))

    @classmethod
    def update_count(cls, count: TokenCount, enc: Encryptor) -> "Token":
        """
        Increases the frequency count of a particular token. If the token
        does not exist this creates the token entry.
        Args:
            count: contains the token and its count.
            enc: an object capable of encrypting and hashing the token.
        """
        token_hash = enc.salted_hash(count["token"])
        try:
            token = cls.get(hash=token_hash)
        except cls.DoesNotExist:
            token = cls.create(
                hash=token_hash, encrypted=enc.encrypt(count["token"])
            )
        token.frequency += count["frequency"]
        token.save()
        return token

    @classmethod
    def get_page(
        cls, page: int, size: int, enc: Encryptor
    ) -> Tuple[List[TokenCount], int]:
        """
        Fetches a page full of tokens and their frequencies from DB, replacing
        the encrypted tokens with their plain text versions.
        Args:
            page: The 0-indexed page number of results.
            size: The number of tokens to include in the page of results.
            enc: an object capable of decrypting tokens.
        """
        print(page, size)
        cursor = (
            cls.select()
            .order_by(cls.frequency.desc())
            .offset((page) * size)
            .limit(size)
        )
        tokens = [cls.decrypt_entry(entry, enc) for entry in cursor]
        total = cls.select().count()
        return tokens, total

    @staticmethod
    def decrypt_entry(entry: "Token", enc: Encryptor) -> TokenCount:
        """
        Decrypts the DB entry of a token.
        Args:
            entry: the DB entry of a token
            enc: an object capable of decrypting the token
        Returns:
            Contains the plain text version of the token, and its frequency
            count.
        """
        decrypted = Token(
            hash=entry.hash,
            encrypted=enc.decrypt(entry.encrypted),
            frequency=entry.encrypted,
        )
        return TokenSchema().dump(decrypted).data

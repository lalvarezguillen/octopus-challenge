from peewee import SqliteDatabase
from octopus.models import URL, Token, db as db
from octopus.crypto import Encryptor
from .test_crypto import CryptoTestsMixin


class MockedEncryptor:
    def encrypt(self, val: str) -> str:
        return val

    def decrypt(self, val: str) -> str:
        return val

    def salted_hash(self, val: str) -> str:
        return val


class TestURL(CryptoTestsMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        test_db = SqliteDatabase(":memory:")
        URL._meta.set_database(test_db)
        db.create_tables([URL])
        cls.enc = Encryptor(cls.private_key_file, "salty")

    @classmethod
    def teardown_class(cls):
        URL._meta.set_database(db)

    def test_get_by_hash_nonexistent(self):
        assert URL.get_by_hash("non-existet.com", self.enc) is None

    def test_get_by_hash(self):
        URL.create(hash=self.enc.salted_hash("asd"), value="asd").save()
        entry = URL.get_by_hash("asd", self.enc)
        assert isinstance(entry, URL)
        assert entry.value == "asd"

    def test_new(self):
        initial_count = URL.select().count()
        entry = URL.new("new.com", self.enc)
        final_count = URL.select().count()
        assert initial_count + 1 == final_count
        assert isinstance(entry, URL)

        queried_entry = URL.get(URL.hash == self.enc.salted_hash("new.com"))
        assert isinstance(queried_entry, URL)


class TestToken(CryptoTestsMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        test_db = SqliteDatabase(":memory:")
        Token._meta.set_database(test_db)
        db.create_tables([Token])
        cls.enc = Encryptor(cls.private_key_file, "salty")

    @classmethod
    def teardown_class(cls):
        Token._meta.set_database(db)

    def test_update_new_token(self):
        initial_count = Token.select().count()
        count = {"token": "dummy", "frequency": 5}
        Token.update_count(count, self.enc)
        final_count = Token.select().count()
        assert initial_count + 1 == final_count

        entry = Token.get(Token.hash == self.enc.salted_hash("dummy"))
        entry.frequency == 5

    def test_updating_existing_token(self):
        Token.update_count({"token": "existing", "frequency": 2}, self.enc)

        initial_count = Token.select().count()
        count = {"token": "existing", "frequency": 5}
        Token.update_count(count, self.enc)
        final_count = Token.select().count()
        assert initial_count == final_count

        entry = Token.get(Token.hash == self.enc.salted_hash("existing"))
        assert entry.frequency == 7

    def test_batch_update(self):
        initial_count = Token.select().count()
        counts = [
            {"token": "batch-update-1", "frequency": 5},
            {"token": "batch-update-2", "frequency": 3},
        ]
        Token.batch_update(counts, self.enc)
        final_count = Token.select().count()
        assert initial_count + len(counts) == final_count

    def test_get_page(self):
        # Clear the table
        Token.delete().execute()

        words = ["Sparta", "Spartan", "Spartacus"]
        counts = [{"token": word, "frequency": 1} for word in words]
        Token.batch_update(counts, self.enc)

        page1, total1 = Token.get_page(0, 1, self.enc)
        page2, total2 = Token.get_page(1, 1, self.enc)
        page3, total3 = Token.get_page(2, 1, self.enc)

        # same page length
        assert len(page1) == len(page2) == len(page3)

        # content differs
        assert page1 != page2 != page3

        # total count is the same
        assert total1 == total2 == total3

        # Data is already decrypted
        assert page1[0]["token"] in words

    def test_decrypt_entry(self):
        count = {"token": "Sparta", "frequency": 5}
        token = Token.update_count(count, self.enc)

        decrypted = Token.decrypt_entry(token, self.enc)
        assert token.encrypted != decrypted["token"]
        assert self.enc.decrypt(token.encrypted) == decrypted["token"]


import tempfile
import os
import Crypto
from Crypto.PublicKey import RSA
from octopus.crypto import Encryptor


class CryptoTestsMixin:
    private_key_file = None

    @classmethod
    def setup_class(cls):
        private = RSA.generate(2048)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(private.exportKey())
        cls.private_key_file = f.name

    @classmethod
    def teardown_class(cls):
        if os.path.isfile(cls.private_key_file):
            os.unlink(cls.private_key_file)


class TestEncryptor(CryptoTestsMixin):
    def test_init(self):
        enc = Encryptor(self.private_key_file, "salty")
        assert isinstance(enc.private, RSA._RSAobj)
        assert isinstance(enc.public, RSA._RSAobj)
        assert enc.salt

    def test_generate_keys(self):
        with open(self.private_key_file, "rb") as f:
            public, private = Encryptor.generate_keys(f.read())
        assert isinstance(public, RSA._RSAobj)
        assert isinstance(private, RSA._RSAobj)

    def test_encrypt_and_decrypt(self):
        enc = Encryptor(self.private_key_file, "salty")
        input = "this is sparta"
        output = enc.decrypt(enc.encrypt(input))
        assert input == output

    def test_salted_hash(self):
        enc = Encryptor(self.private_key_file, "salty")
        hashed = enc.salted_hash("this is sparta")
        assert isinstance(hashed, str)

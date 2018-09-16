import tempfile
import os
import Crypto
from Crypto.PublicKey import RSA
from backend.crypto import Encryptor


class TestEncryptor:
    def test_init(self):
        private = RSA.generate(2048).exportKey()
        enc = Encryptor(private, b"salty")
        assert isinstance(enc.private, RSA._RSAobj)
        assert isinstance(enc.public, RSA._RSAobj)
        assert enc.salt

    def test_generate_keys(self):
        private_b = RSA.generate(2048).exportKey()
        public, private = Encryptor.generate_keys(private_b)
        assert isinstance(public, RSA._RSAobj)
        assert isinstance(private, RSA._RSAobj)

    def test_encrypt_and_decrypt(self):
        private = RSA.generate(2048).exportKey()
        enc = Encryptor(private, b"salty")
        input = "this is sparta"
        output = enc.decrypt(enc.encrypt(input))
        assert input == output

    def test_salted_hash(self):
        private = RSA.generate(2048).exportKey()
        enc = Encryptor(private, b"salty")
        hashed = enc.salted_hash("this is sparta")
        assert isinstance(hashed, str)

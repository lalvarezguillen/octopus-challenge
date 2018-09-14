from typing import List, Tuple
import base64
from hashlib import sha512
import Crypto
from Crypto.PublicKey import RSA
from .config import SALT, PRIVATE_KEY_FILE


def salted_hash(value: str) -> str:
    salt = SALT.encode("utf8")
    return sha512(value.encode("utf8") + salt).hexdigest()


def generate_keys() -> Tuple[RSA._RSAobj, RSA._RSAobj]:
    with open(PRIVATE_KEY_FILE, "rb") as f:
        private = RSA.importKey(f.read())
    public = private.publickey()
    return private, public


PRIVATE, PUBLIC = generate_keys()


def encrypt(value: str) -> str:
    enc = PUBLIC.encrypt(value.encode("utf8"), 32)[0]
    return base64.b64encode(enc).decode("utf8")


def decrypt(value: str) -> str:
    bin_val = base64.b64decode(value.encode("utf8"))
    dec = PRIVATE.decrypt(bin_val)
    return dec.decode("utf8")


CryptoKeys = Tuple[RSA._RSAobj, RSA._RSAobj]


# class Encryptor:
#     def __init__(self, private_key_file: str):
#         with open(private_key_file, "rb") as f:
#             self.private, self.public = self.generate_keys(f.read())

#     def generate_keys(self, primary_key_bin: bytes) -> CryptoKeys:
#         private = RSA.importKey(PRIVATE_KEY)
#         public = private.publickey()
#         return private, public

#     def encrypt(self, value: str) -> str:
#         enc = self.public.encrypt(value.encode("utf8"), 32)[0]
#         return base64.b64encode(enc).decode("utf8")

#     def decrypt(self, value: str) -> str:
#         bin_val = base64.b64decode(value.encode("utf8"))
#         dec = self.private.decrypt(bin_val)
#         return dec.decode("utf8")


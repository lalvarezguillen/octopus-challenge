"""
This module should hold the cryptographic bits of this project.
"""
from typing import List, Tuple
import base64
from hashlib import sha512
import Crypto
from Crypto.PublicKey import RSA


CryptoKeys = Tuple[RSA._RSAobj, RSA._RSAobj]


class Encryptor:
    """
    Initialized with a private RSA key and a salt, this should cover
    the encrypting, hashing and decrypting needs of the project
    """

    def __init__(self, private_key: bytes, salt: bytes):
        """
        Initialize an Encryptor
        Args:
            private_key: The content of a private RSA key.
            salt: a string to use as cryptographic salt
        """
        self.private, self.public = self.generate_keys(private_key)
        self.salt = salt

    @staticmethod
    def generate_keys(private_key_b: bytes) -> CryptoKeys:
        """
        Loads the private RSA key and creates a public key from it.
        Args:
            private_key_bin: The content of the private key, as bytes
        Returns:
            A tuple with the private and public keys
        """
        private = RSA.importKey(private_key_b)
        public = private.publickey()
        return private, public

    def encrypt(self, value: str) -> str:
        """
        Encrypts a value using the public key. It then produces a base64
        string from the encoded bytes, for convenience
        Args:
            value: The string to encrypt
        Returns:
            The base64-encoded and RSA-encrypted string
        """
        enc = self.public.encrypt(value.encode("utf8"), 32)[0]
        return base64.b64encode(enc).decode("utf8")

    def decrypt(self, value: str) -> str:
        """
        Decrypts a base64-encoded and RSA-encrypted string.
        Args:
            value: The string to decrypt
        Returns:
            The decoded and decrypted string
        """
        bin_val = base64.b64decode(value.encode("utf8"))
        dec = self.private.decrypt(bin_val)
        return dec.decode("utf8")

    def salted_hash(self, value: str) -> str:
        """
        Hashes a string with a salt
        """
        return sha512(value.encode("utf8") + self.salt).hexdigest()

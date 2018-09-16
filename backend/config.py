"""
This module loads the project's configurations
"""
import os


class Config:
    # Defines whether Tornado and Celery should be
    # running in debugging mode
    DEBUGGING = bool(os.environ.get("debugging"))

    # Defines the port where the Tornado app should be
    # listening to
    PORT = os.environ["PORT"]

    # Mysql configuration
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = int(os.environ["DB_PORT"])
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]

    # Redis configuration
    REDIS_HOST = os.environ["REDIS_HOST"]

    # A salt to use in the application's hashing.
    SALT_FILE = os.environ["SALT_FILE"]
    SALT = None

    # A private RSA key to use in the application's encryption.
    PRIVATE_KEY_FILE = os.environ["PRIVATE_KEY_FILE"]
    PRIVATE_KEY = None

    def __init__(self):
        with open(self.SALT_FILE, "rb") as f:
            self.SALT = f.read()

        with open(self.PRIVATE_KEY_FILE, "rb") as f:
            self.PRIVATE_KEY = f.read()

    def export(self) -> dict:
        return {
            "DEBUGGING": self.DEBUGGING,
            "PORT": self.PORT,
            "DB_HOST": self.DB_HOST,
            "DB_PORT": self.DB_PORT,
            "DB_NAME": self.DB_NAME,
            "DB_USER": self.DB_USER,
            "DB_PASS": self.DB_PASS,
            "REDIS_HOST": self.REDIS_HOST,
            "SALT": self.SALT,
            "PRIVATE_KEY": self.PRIVATE_KEY,
        }


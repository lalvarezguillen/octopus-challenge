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
    SALT = os.environ["SALT"]

    # A private RSA key to use in the application's encryption.
    PRIVATE_KEY = os.environ["PRIVATE_KEY"]

    @classmethod
    def export(cls) -> dict:
        return {
            "DEBUGGING": cls.DEBUGGING,
            "PORT": cls.PORT,
            "DB_HOST": cls.DB_HOST,
            "DB_PORT": cls.DB_PORT,
            "DB_NAME": cls.DB_NAME,
            "DB_USER": cls.DB_USER,
            "DB_PASS": cls.DB_PASS,
            "REDIS_HOST": cls.REDIS_HOST,
            "SALT": cls.SALT,
            "PRIVATE_KEY": cls.PRIVATE_KEY,
        }

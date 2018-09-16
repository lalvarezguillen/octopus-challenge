"""
This module loads the project's configurations
"""
import os


class Config:
    DEBUGGING = bool(os.environ.get("debugging"))
    PORT = os.environ["PORT"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = int(os.environ["DB_PORT"])
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    REDIS_HOST = os.environ["REDIS_HOST"]
    SALT = os.environ["SALT"]
    PRIVATE_KEY = os.environ["PRIVATE_KEY"]

    @classmethod
    def export(cls):
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

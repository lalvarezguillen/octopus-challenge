"""
This module loads the project's configurations
"""
import os


class Config:
    PORT = os.environ["PORT"]
    DB_HOST = os.environ["DB_HOST"]
    REDIS_HOST = os.environ["REDIS_HOST"]
    SALT = os.environ["SALT"]
    PRIVATE_KEY_FILE = os.environ["PRIVATE_KEY_FILE"]

    @classmethod
    def export(cls):
        return {
            "PORT": cls.PORT,
            "DB_HOST": cls.DB_HOST,
            "REDIS_HOST": cls.REDIS_HOST,
            "SALT": cls.SALT,
            "PRIVATE_KEY_FILE": cls.PRIVATE_KEY_FILE,
        }

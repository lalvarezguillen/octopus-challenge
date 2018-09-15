"""
This module contains code to set up tornado and celery.
"""
import os
import tornado.ioloop
import tornado.web
from .handlers import MainHandler, TokensHandler, AnalysisHandler
from .config import Config
from .models import BaseModel, URL, Token, db
from .jobs import CELERY
from .crypto import Encryptor


def make_app():
    """
    Creates the Tornado app, updates Celery's settings and sets up the DB.
    """
    static_path = os.path.join(
        os.path.dirname(__file__), os.pardir, "frontend", "dist"
    )
    print(static_path)
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/tokens", TokensHandler),
            (r"/tasks/?", AnalysisHandler),
            (r"/tasks/(?P<task_id>[a-zA-Z0-9\-_]+)", AnalysisHandler),
        ],
        debug=True,
        static_path=static_path,
        encryptor=Encryptor(Config.PRIVATE_KEY_FILE, Config.SALT),
    )
    app.settings.update(Config.export())
    CELERY.conf.update(app.settings)
    CELERY.conf.update()

    return app


def setup_db():
    """
    Sets up the DB
    """
    db.init(Config.DB_HOST)
    db.connect()
    db.create_tables([URL, Token])


def run_app():
    """
    Starts running the tornado app
    """
    app = make_app()
    app.listen(Config.PORT)
    tornado.ioloop.IOLoop.current().start()

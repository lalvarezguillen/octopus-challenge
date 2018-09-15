import os
import tornado.ioloop
import tornado.web
from .handlers import MainHandler, TokensHandler, AnalysisHandler
from .config import PORT
from .models import db, URL, Token


def make_app():
    static_path = os.path.join(
        os.path.dirname(__file__), os.pardir, "frontend", "dist"
    )
    print(static_path)
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/tokens", TokensHandler),
            (r"/task/?", AnalysisHandler),
            (r"/task/(?P<task_id>[a-zA-Z0-9\-_]+)", AnalysisHandler),
        ],
        debug=True,
        static_path=static_path,
    )


def run_app():
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

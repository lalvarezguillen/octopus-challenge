import tornado.ioloop
import tornado.web
from .handlers import MainHandler, AdminHandler
from .config import PORT


def make_app():
    return tornado.web.Application(
        [(r"/", MainHandler), (r"/admin", AdminHandler)]
    )


def run_app():
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

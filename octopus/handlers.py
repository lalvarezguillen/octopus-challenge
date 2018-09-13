import json
import tornado
import tornado.web
from .schemas import URLSchema


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        payload = tornado.escape.json_decode(self.request.body)
        parsed = URLSchema().load(payload)
        self.set_header("Content-Type", "application/json")
        if parsed.errors:
            self.set_status(400)
            self.finish(tornado.escape.json_encode(parsed.errors))
        else:
            self.finish(tornado.escape.json_encode({}))
            self.set_status(202)


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        pass

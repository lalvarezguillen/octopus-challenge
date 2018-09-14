import json
import tornado
import tornado.web
from .schemas import TaskRequestSchema
from .jobs import CELERY, frequency_analysis, sentiment_analysis
from .models import Token
from .helpers import parse_pagination


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")


class AnalysisHandler(tornado.web.RequestHandler):
    def get(self, task_id=None):
        if not task_id:
            self.set_status(404)
            self.finish()
            return

        task = CELERY.AsyncResult(task_id)
        self.set_header("Content-Type", "application/json")

        if not task.ready():
            self.set_status(204)
            self.finish()
            return

        self.set_status(200)
        self.finish(task.result)

    def post(self, **_):
        parsed = TaskRequestSchema().loads(self.request.body)
        self.set_header("Content-Type", "application/json")
        if parsed.errors:
            self.set_status(400)
            self.finish(tornado.escape.json_encode(parsed.errors))
            return

        task = frequency_analysis.delay(parsed.data["url"])
        self.set_status(202)
        self.finish(tornado.escape.json_encode({"id": task.id}))


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        page = parse_pagination(self.get_query_argument("page", 1))
        size = parse_pagination(self.get_query_argument("size", 50))
        content = Token.get_page(page, size)
        self.set_status(202)
        self.finish(tornado.escape.json_encode(content))

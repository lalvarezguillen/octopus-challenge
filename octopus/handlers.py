"""
Contains the http handlers of this application
"""
import json
import tornado
import tornado.web
from .schemas import TaskRequestSchema, TaskResultSchema
from .jobs import CELERY, frequency_analysis, sentiment_analysis
from .models import Token
from .helpers import parse_pagination


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """
        Renders the landing page.
        """
        self.render("main.html")


class AnalysisHandler(tornado.web.RequestHandler):
    def get(self, task_id=None):
        """
        Handles fetching the state & result of a web page analysis
        """
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
        self.finish(tornado.escape.json_encode(task.result))

    def post(self, **_):
        """
        Handles queuing up a web page for analysis
        """
        parsed = TaskRequestSchema().loads(self.request.body)
        self.set_header("Content-Type", "application/json")
        if parsed.errors:
            self.set_status(400)
            self.finish(tornado.escape.json_encode(parsed.errors))
            return

        task = frequency_analysis.delay(parsed.data["url"])
        self.set_status(202)
        self.finish(tornado.escape.json_encode({"id": task.id}))


class TokensHandler(tornado.web.RequestHandler):
    def get(self):
        """
        Handles fetching paginated list of tokens and their frequencies.
        """
        page = parse_pagination(self.get_query_argument("page", 1))
        size = parse_pagination(self.get_query_argument("size", 50))
        encryptor = self.application.settings["encryptor"]
        tokens, total = Token.get_page(page, size, encryptor)
        resp = {"tokens": tokens, "total": total}
        self.set_status(200)
        self.finish(tornado.escape.json_encode(resp))

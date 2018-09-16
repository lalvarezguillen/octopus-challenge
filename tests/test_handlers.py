import json
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.httpserver import HTTPRequest
from unittest import mock
from backend.app import make_app
import backend.handlers


class TestMainHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_get_ok(self):
        resp = self.fetch("/")
        assert resp.code == 200


@mock.patch("backend.handlers.frequency_analysis")
@mock.patch("backend.handlers.CELERY")
class TestAnalysisHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_get_missing_task_id(self, *_):
        resp = self.fetch("/tasks")
        assert resp.code == 404

    def test_get_task_not_ready(self, celery_mock, *_):
        task_mock = mock.MagicMock()
        task_mock.ready.return_value = False
        celery_mock.AsyncResult.return_value = task_mock

        resp = self.fetch("/tasks/some-task")
        assert resp.code == 204

    def test_get_task_ready(self, celery_mock, *_):
        task_mock = mock.MagicMock()
        task_mock.ready.return_value = True
        dummy_result = {"done": True}
        task_mock.result = dummy_result
        celery_mock.AsyncResult.return_value = task_mock

        resp = self.fetch("/tasks/some-task")
        assert resp.code == 200
        assert json.loads(resp.body) == dummy_result

    def test_post_task_malformed_payload(self, *_):
        payload = ["this is", "sparta"]

        resp = self.fetch("/tasks", method="POST", body=json.dumps(payload))
        assert resp.code == 400

    def test_post_task(self, celery_mock, freq_analysis_mock):
        mocked_task = mock.MagicMock()
        mocked_task.id = "dummy-task"
        freq_analysis_mock.delay.return_value = mocked_task

        payload = {"url": "http://dummy.com"}
        resp = self.fetch("/tasks", method="POST", body=json.dumps(payload))
        assert resp.code == 202
        resp_body = json.loads(resp.body)
        assert resp_body["id"] == "dummy-task"


@mock.patch("backend.handlers.Token")
class TestTokensHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_get_(self, mocked_token):
        tokens = [
            {"token": "sparta", "frequency": 2},
            {"token": "tomato", "frequency": 14},
        ]
        total = 10
        mocked_token.get_page.return_value = (tokens, total)

        resp = self.fetch("/tokens?size=2&page1")
        assert resp.code == 200
        resp_body = json.loads(resp.body)
        assert list(  # There's an element with with token==tomato in the list
            filter(lambda x: x["token"] == "tomato", resp_body["tokens"])
        )
        assert resp_body["total"] == total

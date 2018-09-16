from unittest import mock
import pytest
import backend.helpers
from backend.helpers import parse_pagination, retry


def test_parse_pagination():
    cases = [
        {"in": "1", "exp": 1},
        {"in": "-1", "exp": 0},
        {"in": "a", "exp": 0},
        {"in": [], "exp": 0},
    ]
    for case in cases:
        outp = parse_pagination(case["in"])
        assert outp == case["exp"]


@mock.patch("backend.helpers.time")
class TestRetry:
    def test_returns_result(self, mocked_time):
        func = lambda: 2 / 2
        result = retry(func, (ZeroDivisionError,))
        assert result == 1

    def test_raises_error(self, mocked_time):
        func = lambda: 2 / 0
        with pytest.raises(ZeroDivisionError) as err:
            retry(func, (ZeroDivisionError,))
            assert err


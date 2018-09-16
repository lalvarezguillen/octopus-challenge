from backend.helpers import parse_pagination


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


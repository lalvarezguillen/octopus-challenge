"""
Contains generic helpers for this project
"""


def parse_pagination(arg: str) -> int:
    """
    Parses a parameter involved in paginating a query.
    These kind of parameters need to be integers greater
    than zero.

    Args:
        arg: The value of the pagination parameter.
    Returns:
        The clean pagination parameter
    """
    try:
        int_arg = int(arg)
    except (TypeError, ValueError):
        int_arg = 0

    if int_arg < 0:
        return 0
    return int_arg

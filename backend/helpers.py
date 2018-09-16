"""
Contains generic helpers for this project
"""
import time
import math
from typing import Callable, Tuple, Any


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


def retry(operation: Callable, errors: Tuple[BaseException, ...], times: int=1) -> Any:
    '''
    Retries an operation up N times if errors of particular types come up.
    Args:
        operation: The operation that will be retried. It should be a function
        that takes no arguments.
        errors: a list of retriable errors
        times: The max number of times that operation will be retried
    Returns:
        Whatever operation() returns
    '''
    tries = 0
    while True:
        try:
            return operation()
        except errors as err:
            if tries == times:
                raise err
            print(f'retrying {operation}')
            time.sleep(math.pow(5, tries))
            tries += 1

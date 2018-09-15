def parse_pagination(arg: str) -> int:
    int_arg = int(arg)
    if int_arg < 0:
        return 0
    return int_arg

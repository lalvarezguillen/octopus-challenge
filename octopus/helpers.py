def parse_pagination(arg: str) -> int:
    int_arg = int(arg)
    if int_arg <= 0:
        return 1
    return int_arg

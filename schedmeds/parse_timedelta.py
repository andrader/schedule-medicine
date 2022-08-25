import re
import datetime as dt

_PATTERN = (
    r"^(?!\d*$)" # negative lookahead: garante que nao é str vazia ou só digitos: '', '1'
    r"(?:(?P<days>\d+)\s*(?:d|days?),?\s*)?"
    r"(?:(?P<hours>\d+)[:h])?"
    r"(?:(?P<minutes>\d+)[:m]?)?"
    r"(?:(?P<seconds>\d*)s?)?"
    r"$"
)

_COMPILED_PATTERN = re.compile(_PATTERN, re.IGNORECASE)


def parse_timedelta(string):
    if isinstance(string, dt.timedelta):
        return string

    matchs = re.match(_COMPILED_PATTERN, string)
    if not matchs:
        raise ValueError(f"couldn't parse time '{string}'")

    matchs = matchs.groupdict()
    parts = {name: int(param) for name, param in matchs.items() if param}

    return dt.timedelta(**parts)


def test_timedelta_convertion():
    print('testing dt.timedelta conversions')

    for i in [0, 1, 23, 72]:
        for param in ["days", "hours", "minutes"]:
            d = dt.timedelta(**{param: i})
            if not d == parse_timedelta(str(d)):
                return False
    
    return True




def test_valid_strings():
    print("testing valid strings")

    ss = {
        "0 days": "0:00:00",
        "1 day": "1 day, 0:00:00",
        "2 days": "2 days, 0:00:00",
        "998 days": "998 days, 0:00:00",
        "30 days 0h": "30 days, 0:00:00",
        "30 days 0:": "30 days, 0:00:00",
        "30 days 1h": "30 days, 1:00:00",
        "30 days 1:": "30 days, 1:00:00",
        "30 days 3h": "30 days, 3:00:00",
        "30 days 3:": "30 days, 3:00:00",
        "30 days 3h05": "30 days, 3:05:00",
        "30 days 3:05": "30 days, 3:05:00",
        "30 days 3h05m": "30 days, 3:05:00",
        "30 days 3:05m": "30 days, 3:05:00",
        "30 days 3:05m50s": "30 days, 3:05:50",
        "30 days 50s": "30 days, 0:50:00",
    }

    eq = [parse_timedelta(k)==parse_timedelta(v) for k,v in ss.items()]

    return all(eq)


def test_invalid_strings():
    print("testing invalid strings")
    ss = ["", " ", "fsdfs", "1", "   12  "]

    for s in ss:
        passed = False
        try:
            parse_timedelta(s)
        except ValueError as e:
            passed = True
        
        if not passed:
            return False
    
    return True


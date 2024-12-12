import re


def _validate_username(username: str, blacklist: list[str]) -> bool:
    p = re.compile(r'[a-zA-Z\u0590-\u05fe0-9]+$')
    m = p.match(username)
    return bool(m) and username not in blacklist

def validate_user(username: str, password: str, blacklist: list[str]) -> bool:
    is_username_valid = _validate_username(username, blacklist)
    is_matan = username == "matmat18"

    return is_username_valid and ((is_matan and password == "vinkvink123") or (not is_matan and password == "nignig123"))

def exclude_client(exclude_client):
    def wrapper(client):
        return client != exclude_client
    return wrapper
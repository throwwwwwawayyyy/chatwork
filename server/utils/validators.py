import re

def validate_username(username: bytes) -> bool:
    p = re.compile(r'[a-z\u0590-\u05fe0-9]+$')
    m = p.match(username.decode('utf-8'))
    return bool(m)

def validate_password(password: str):
    return password == b'nignig123'
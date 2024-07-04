import re
from objects.messages import AckMessage
from utils import constants

def validate_username(username: bytes) -> bool:
    p = re.compile(r'[a-zA-Z\u0590-\u05fe0-9]+$')
    m = p.match(username.decode('utf-8'))
    return bool(m)

def validate_password(password: bytes) -> bool:
    return password == b'nignig123'

def validate_credentials(username: bytes, password: bytes) -> bool:
    if validate_username(username) and validate_password(password):
        return True
    return False

def exclude_client(exclude_client):
    def wrapper(client):
        print(client.username, exclude_client.username)
        return client != exclude_client
    return wrapper
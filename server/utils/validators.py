import re
from objects.messages import AuthMessage
from utils import constants

def validate_username(username: str) -> bool:
    p = re.compile(r'[a-zA-Z\u0590-\u05fe0-9]+$')
    m = p.match(username)
    return bool(m)

def validate_password(password: str) -> bool:
    return password == 'nignig123'

def validate_credentials(auth_message: AuthMessage) -> bool:
    if validate_username(auth_message.username) and validate_password(auth_message.password):
        return True
    return False

def exclude_client(exclude_client):
    def wrapper(client):
        return client != exclude_client
    return wrapper
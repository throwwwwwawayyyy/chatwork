from enum import Enum


class AckCodes(Enum):
    CREDENTIALS_DENIED = 0
    CREDENTIALS_ACCEPTED = 1
    CLIENT_DENIED = 4
    CLIENT_AUTHORIZED = 5
    ERROR = 6


class MessageType(Enum):
    FALLBACK = -1
    ACK = 0
    CLIENT = 1
    SERVER = 2
    JOIN = 3
    LEAVE = 4
    AUTH = 5
    
    
class Privileges(Enum):
    DEFAULT = 0
    ADMIN = 1


class State(Enum):
    AUTH = 0
    CONNECTED = 1


SEP = "&@^"

RSA_KEY_DEFAULT_SIZE = 1024
RSA_KEY_END_HEADER = b"\n-----END RSA PUBLIC KEY-----\n"
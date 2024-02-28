from enum import Enum


class AckCodes(Enum):
    CREDENTIALS_DENIED = 0
    CREDENTIALS_ACCEPTED = 1
    CLIENT_DENIED = 4
    CLIENT_AUTHORIZED = 5
    ERROR = 6


class MessageType(Enum):
    ACK = 0
    CLIENT = 1
    SERVER = 2
    JOIN = 3
    LEAVE = 4
    
    
class Privileges(Enum):
    DEFAULT = 0
    ADMIN = 1


SEP = "&@^"
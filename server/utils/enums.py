from enum import Enum


class AckCode(Enum):
    CREDENTIALS_DENIED = 0
    CREDENTIALS_ACCEPTED = 1
    CLIENT_DENIED = 4
    CLIENT_AUTHORIZED = 5
    ERROR = 6
    COMMAND_FAIL = 7
    COMMAND_SUCCESS = 8


class MessageType(Enum):
    FALLBACK = -1
    ACK = 0
    CLIENT = 1
    SERVER = 2
    JOIN = 3
    LEAVE = 4
    AUTH = 5
    COMMAND = 6
    DISCONNECT = 7
    SYSTEM = 8
    
    
class Privilege(Enum):
    DEFAULT = 0
    MOD = 1
    ADMIN = 2
    ROOT = 3

    def promote(self):
        try:
            return Privilege(self.value + 1)
        except ValueError:
            return self
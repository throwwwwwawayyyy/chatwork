from enum import Enum

class MessageType(Enum):
    ACK = 0
    CLIENT = 1
    SERVER = 2
    JOIN = 3

class Privileges(Enum):
    DEFAULT = 0
    ADMIN = 1

SYSTEM_USER = "System"
YOUR_USER = "You"

USERNAME_LEVEL = 0
PASSWORD_LEVEL = 1
WAITING_LEVEL = 2
CHAT_LEVEL = 3

SEP = "&@^"

EXIT_MESSAGE = "exit"

DEBUG_KEYWORD = "-debug"

PASSWORD_DISPLAY_CHARACTER = "*"
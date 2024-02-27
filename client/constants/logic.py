from enum import Enum

class MessageType(Enum):
    ACK = 0
    CLIENT = 1
    SERVER = 2
    JOIN = 3

SYSTEM_USER = "System"
SERVER_USER = "Server"
YOUR_USER = "You"

USERNAME_LEVEL = 0
PASSWORD_LEVEL = 1
WAITING_LEVEL_1 = 2
WAITING_LEVEL_2 = 3
CHAT_LEVEL = 4

SEP = "&@^"

EXIT_MESSAGE = "exit"

DEBUG_KEYWORD = "-debug"
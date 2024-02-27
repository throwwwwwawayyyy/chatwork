from enum import Enum


class AckCodes(Enum):
    CREDENTIALS_DENIED = 0
    CREDENTIALS_ACCEPTED = 1
    WHITELIST_OFF = 2
    WHITELIST_ON = 3
    CLIENT_DENIED = 4
    CLIENT_AUTHORIZED = 5
    ERROR = 6


class MessageType(Enum):
    ACK = 0
    CLIENT = 1
    SERVER = 2
    JOIN = 3


PASSWORD_LEVEL = 0
USERNAME_LEVEL = 1
WAITING_LEVEL_1 = 2
WAITING_LEVEL_2 = 3
CHAT_LEVEL = 4

SEP = "&@^"

EXIT_MESSAGE = "exit"

DEBUG_KEYWORD = "-debug"

INPUT_HINT_TEXT = f"Type a message (or type '{EXIT_MESSAGE}' to exit): "
PASSWORD_HINT_TEXT = f"Type a password (or type '{EXIT_MESSAGE}' to exit): "
USERNAME_HINT_TEXT = f"Type a username (or type '{EXIT_MESSAGE}' to exit): "
WAITING_HINT_TEXT = f"Waiting for admin approval (type '{EXIT_MESSAGE}' to exit): "

WRONG_PASSWORD_TEXT = "Wrong password."
CORRECT_PASSWORD_TEXT = "Correct password."
USERNAME_DENIED_TEXT = "Username denied."
USERNAME_ACCEPTED_TEXT = "Username accepted."
WHITELIST_ON_TEXT = "Waiting for admin approval..."
WHITELIST_OFF_TEXT = "Something went wrong."
CLIENT_DENIED_TEXT = "Client denied."
CLIENT_AUTHORIZED_TEXT = "Client authorised."
NULL_MESSAGE_TEXT = "NULL"

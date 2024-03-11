from constants.logic import SEP, SYSTEM_USER
from constants.texts import *
from constants.ack_codes import ack_to_text, errored_ack_codes
from constants.colors import CLIColors

from utils.build_message import build_message

class Message:
    error: bool
    color: int
    keep_color: bool

    def __init__(self, encoded_msg: str) -> None:
        self.error = False
        self.color = CLIColors.DEFAULT_COLOR.value
        self.keep_color = False

    def __str__(self) -> str:
        return None

class ClientMessage(Message):
    username: str
    content: str

    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)
        _, self.username, self.content = encoded_msg.split(SEP)

    def __str__(self) -> str:
        return build_message(self.username, self.content)

class AckMessage(Message):
    content: int

    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)

        _, self.content = encoded_msg.split(SEP)
        self.content = int(self.content)

        self.error = (self.content in errored_ack_codes)
        if self.error:
            self.color = CLIColors.ERROR_COLOR.value
            self.keep_color = True
        else:
            self.color = CLIColors.SYSTEM_MESSAGE_COLOR.value
            self.keep_color = True

    def __str__(self) -> str:
        return build_message(SYSTEM_USER, ack_to_text[self.content])

class JoinMessage(Message):
    username: str
    privilege: int

    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)

        _, self.username, self.privilege = encoded_msg.split(SEP)
        self.privilege = int(self.privilege)
        
        self.color = CLIColors.SYSTEM_MESSAGE_COLOR.value
        self.keep_color = True

    def __str__(self) -> str:
        return build_message(SYSTEM_USER, self.username + JOINED_MSG_TEXT)
    
class InvalidMessage(Message):
    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)
        
        self.error = True
        self.color = CLIColors.ERROR_COLOR.value
        self.keep_color = True
        
    def __str__(self) -> str:
        return build_message(SYSTEM_USER, INVALID_MESSAGE_TEXT)
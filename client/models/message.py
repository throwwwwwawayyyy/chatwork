from constants.logic import SEP, SYSTEM_USER
from constants.texts import *
from constants.ack_codes import ack_to_text, errored_ack_codes

class Message:
    error: bool

    def __init__(self, encoded_msg: str) -> None:
        self.error = False

    def __str__(self) -> str:
        print("Not implemented")
        return None

class ClientMessage(Message):
    username: str
    content: str

    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)
        _, self.username, self.content = encoded_msg.split(SEP)

    def __str__(self) -> str:
        return f"{self.username}: {self.content}"

class AckMessage(Message):
    content: int

    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)

        _, self.content = encoded_msg.split(SEP)
        self.content = int(self.content)

        self.error = (self.content in errored_ack_codes)

    def __str__(self) -> str:
        return f"[{SYSTEM_USER}]: {ack_to_text[self.content]}"

class JoinMessage(Message):
    username: str
    privilege: int

    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)

        _, self.username, self.privilege = encoded_msg.split(SEP)
        self.privilege = int(self.privilege)

    def __str__(self) -> str:
        return f"[{SYSTEM_USER}]: {self.username} joined!"
    
class InvalidMessage(Message):
    def __init__(self, encoded_msg: str) -> None:
        super().__init__(encoded_msg)
        self.error = True
        
    def __str__(self) -> str:
        return f"[{SYSTEM_USER}]: {INVALID_MESSAGE_TEXT}"
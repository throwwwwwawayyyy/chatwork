from constants.logic import SEP
from constants.texts import *
from models.ack_codes import ack_to_text, errored_ack_codes

class Message:
    error: bool

    def __init__(self, encoded_msg) -> None:
        self.error = False

    def __str__(self) -> str:
        print("Not implemented")
        return None

class ClientMessage(Message):
    username: str
    content: str
    ip: str
    port: str

    def __init__(self, encoded_msg: str) -> None:
        super.__init__(encoded_msg)
        _, self.ip, self.port, self.username, self.content = encoded_msg.split(SEP)

    def __str__(self) -> str:
        return f"{self.username}: {self.content}"

class AckMessage(Message):
    content: int

    def __init__(self, encoded_msg: str) -> None:
        super.__init__(encoded_msg)

        _, self.content = encoded_msg.split(SEP)
        self.content = int(self.content)

        self.error = (self.content in errored_ack_codes)

    def __str__(self) -> str:
        return ack_to_text[self.content]

class JoinMessage(Message):
    ip: str
    port: str
    username: str
    privilage: str

    def __init__(self, encoded_msg: str) -> None:
        super.__init__(encoded_msg)

        _, self.ip, self.port, self.username, self.privilage = encoded_msg.split(SEP)

    def __str__(self) -> str:
        return f"{self.username} joined!"
from dataclasses import dataclass
import utils.constants as constants


class Message:
    def serialize(self):
        print("Don't instanciate a Message type directly. Use a subclass")


@dataclass
class ClientMessage(Message):
    content: bytes
    ip: str
    port: str

    def serialize(self) -> bytes:
        result = f"{constants.MessageType.CLIENT}{constants.SEP}\
                   {self.ip}{constants.SEP}\
                   {self.port}{constants.SEP}\
                   {self.content}"
        return result.encode('utf-8')


@dataclass
class AckMessage(Message):
    content: int

    def serialize(self):
        result = f"{constants.MessageType.ACK}{constants.SEP}\
                   {self.content}"
        return result.encode('utf-8')


@dataclass
class JoinMessage(Message):
    username: str
    privilage: str

    def serialize(self):
        result = f"{constants.MessageType.CLIENT}{constants.SEP}\
                   {self.username}{constants.SEP}\
                   {self.privilage}"
        return result.encode('utf-8')

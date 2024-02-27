from dataclasses import dataclass
import utils.constants as constants


class Message:
    def serialize(self):
        print("Don't instanciate a Message type directly. Use a subclass")


@dataclass
class ClientMessage(Message):
    content: bytes
    username: str

    def serialize(self) -> bytes:
        result = f"{constants.MessageType.CLIENT.value}{constants.SEP}\
                   {self.username}{constants.SEP}\
                   {self.content}"
        return result.encode('utf-8')


@dataclass
class AckMessage(Message):
    content: constants.AckCodes

    def serialize(self):
        result = f"{constants.MessageType.ACK.value}{constants.SEP}\
                   {self.content.value}"
        return result.encode('utf-8')


@dataclass
class JoinMessage(Message):
    username: str
    privilage: int

    def serialize(self):
        result = f"{constants.MessageType.CLIENT.value}{constants.SEP}\
                   {self.username}{constants.SEP}\
                   {self.privilage}"
        return result.encode('utf-8')

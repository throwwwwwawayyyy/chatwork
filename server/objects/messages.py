from dataclasses import dataclass
import utils.constants as constants


class Message:
    def serialize(self):
        print("Don't instantiate a Message type directly. Use a subclass")


@dataclass
class ClientMessage(Message):
    username: str
    content: bytes

    def serialize(self) -> bytes:
        result = f"{constants.MessageType.CLIENT.value}{constants.SEP}{self.username}{constants.SEP}{self.content.decode('utf-8')}"
        return result.encode('utf-8')


@dataclass
class AckMessage(Message):
    code: constants.AckCodes

    def serialize(self) -> bytes:
        result = f"{constants.MessageType.ACK.value}{constants.SEP}{self.code.value}"
        return result.encode('utf-8')


@dataclass
class JoinMessage(Message):
    username: str
    privilage: int

    def serialize(self) -> bytes:
        result = f"{constants.MessageType.JOIN.value}{constants.SEP}{self.username}{constants.SEP}{self.privilage}"
        return result.encode('utf-8')


@dataclass
class LeaveMessage(Message):
    username: str

    def serialize(self) -> bytes:
        result = f"{constants.MessageType.LEAVE.value}{constants.SEP}{self.username}"
        return result.encode('utf-8')

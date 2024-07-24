from dataclasses import dataclass, asdict
import json
import utils.constants as constants


class Message:
    def __init__(self):
        print("Don't instantiate this class directly, use a subclass")

    def serialize(self) -> bytes:
        result = asdict(self)
        result["type"] = type(self)
        return bytes(json.dumps(result))
    
    def from_bytes(encoded_msg: bytes):
        message_dict = json.loads(str(encoded_msg))
        message_type = message_dict["type"]
        print(message_type)


@dataclass
class ClientMessage(Message):
    username: str
    content: bytes

    @staticmethod
    def _from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(str(encoded_msg))
        username = message_dict["username"]
        content = message_dict["content"]
        return ClientMessage(username, content)


@dataclass
class AckMessage(Message):
    code: constants.AckCodes

    @staticmethod
    def _from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(str(encoded_msg))
        code = message_dict["code"]
        return AckMessage(code)


@dataclass
class JoinMessage(Message):
    username: str
    privilege: int

    @staticmethod
    def _from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(str(encoded_msg))
        username = message_dict["username"]
        privilege = message_dict["privilege"]
        return JoinMessage(username, privilege)


@dataclass
class LeaveMessage(Message):
    username: str

    @staticmethod
    def _from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(str(encoded_msg))
        username = message_dict["username"]
        return LeaveMessage(username)

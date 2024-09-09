from dataclasses import dataclass, asdict
import json
from utils.constants import MessageType
import logging


logger = logging.getLogger(__name__)


class Message:
    def __init__(self):
        logger.debug("Don't instantiate the Message class directly, use a subclass")

    def serialize(self) -> bytes:
        result = asdict(self)
        result["type"] = type(self).msg_type
        return bytes(json.dumps(result), "utf-8")
    
    def from_bytes(encoded_msg: bytes):
        message_dict = json.loads(encoded_msg.decode("utf-8"))
        message_type = message_dict.get("type")
        try:
            match int(message_type):
                case MessageType.CLIENT.value:
                    return ClientMessage.from_bytes(encoded_msg)
                case MessageType.AUTH.value:
                    return AuthMessage.from_bytes(encoded_msg)
                case _:
                    raise ValueError("Invalid message type")
        except ValueError:
            return FallbackMessage()
        

@dataclass
class AuthMessage(Message):
    msg_type = MessageType.AUTH.value
    username: str
    password: str

    @staticmethod
    def from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(encoded_msg.decode("utf-8"))
        username = message_dict["username"]
        password = message_dict["password"]
        return AuthMessage(username, password)


@dataclass
class ClientMessage(Message):
    msg_type = MessageType.CLIENT.value
    username: str
    content: bytes

    @staticmethod
    def from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(encoded_msg.decode("utf-8"))
        username = message_dict["username"]
        content = message_dict["content"]
        return ClientMessage(username, content)


@dataclass
class AckMessage(Message):
    msg_type = MessageType.ACK.value
    code: int
    @staticmethod
    def from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(encoded_msg.decode("utf-8"))
        code = message_dict["code"]
        return AckMessage(code)


@dataclass
class JoinMessage(Message):
    msg_type = MessageType.JOIN.value
    username: str
    privilege: int

    @staticmethod
    def from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(encoded_msg.decode("utf-8"))
        username = message_dict["username"]
        privilege = message_dict["privilege"]
        return JoinMessage(username, privilege)


@dataclass
class LeaveMessage(Message):
    msg_type = MessageType.LEAVE.value
    username: str

    @staticmethod
    def from_bytes(encoded_msg: bytes) -> None:
        message_dict = json.loads(encoded_msg.decode("utf-8"))
        username = message_dict["username"]
        return LeaveMessage(username)
    

class FallbackMessage(Message):
    msg_type = MessageType.FALLBACK.value
    
    def __init__(self):
        logger.debug("Don't instantiate the Message class directly, use a subclass")

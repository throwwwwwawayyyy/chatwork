from dataclasses import dataclass, asdict
import json
import utils.constants as constants


class Message:
    def __init__(self):
        print("Don't instantiate this class directly, use a subclass")

    def serialize(self) -> bytes:
        return bytes(json.dumps(asdict(self)))


@dataclass
class ClientMessage(Message):
    username: str
    content: bytes


@dataclass
class AckMessage(Message):
    code: constants.AckCodes


@dataclass
class JoinMessage(Message):
    username: str
    privilege: int


@dataclass
class LeaveMessage(Message):
    username: str

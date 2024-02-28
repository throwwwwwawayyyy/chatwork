from dataclasses import dataclass
from objects.messages import Message

@dataclass
class MessageReceivedEvent:
    message: Message
    ip: str
    

@dataclass
class UserJoinedEvent:
    client: object
from dataclasses import dataclass
from objects.messages import Message

@dataclass
class MessageReceivedEvent:
    message: Message
    

@dataclass
class UserJoinedEvent:
    username: str
    privilage: str
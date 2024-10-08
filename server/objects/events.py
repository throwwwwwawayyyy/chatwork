from dataclasses import dataclass
from objects.messages import Message

@dataclass
class MessageReceivedEvent:
    message: Message
    client: object


@dataclass
class ClientJoinAttemptEvent:
    client: object


@dataclass
class ClientJoinEvent:
    client: object


@dataclass
class ClientLeaveEvent:
    client: object
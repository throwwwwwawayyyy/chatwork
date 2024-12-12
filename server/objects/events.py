from dataclasses import dataclass
from objects.messages import Message
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.client_manager import ClientManager

@dataclass
class MessageReceivedEvent:
    message: Message
    client: "ClientManager"


@dataclass
class ClientJoinAttemptEvent:
    client: "ClientManager"


@dataclass
class ClientJoinEvent:
    client: "ClientManager"


@dataclass
class ClientDisconnectEvent:
    client: "ClientManager"
    

@dataclass
class ServerStopEvent:
    pass
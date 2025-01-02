from dataclasses import dataclass
from objects.messages import Message
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.client_manager import ClientManager
    from managers.group_manager import GroupManager

@dataclass
class MessageReceivedEvent:
    message: Message
    client: 'ClientManager'


@dataclass
class ClientJoinServerEvent:
    client: 'ClientManager'


@dataclass
class ClientDisconnectEvent:
    client: 'ClientManager'
    

@dataclass
class ServerStopEvent:
    pass

@dataclass
class GroupCreateEvent:
    group: 'GroupManager'

@dataclass
class ClientLeaveGroupEvent:
    client: 'ClientManager'
    group: 'GroupManager'

@dataclass
class ClientChangeActiveGroupEvent:
    client: 'ClientManager'
    group: 'GroupManager'

@dataclass
class GroupCloseEvent:
    group: 'GroupManager'
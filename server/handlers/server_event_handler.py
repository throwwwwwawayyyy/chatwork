import logging
from managers.event_manager import EventManager
from objects.messages import ClientMessage, JoinMessage, LeaveMessage, CommandMessage, DisconnectMessage, Message
from utils import validators
from objects.events import *
from managers.command_manager import CommandManager
from managers.client_manager import ClientManager
from utils import utils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.server_manager import ServerManager

class ServerEventHandler:
    def __init__(self, 
                 event_manager: EventManager,
                 command_manager: CommandManager,
                 server_manager: 'ServerManager') -> None:
        self.logger = logging.getLogger(__name__)
        self.server_manager = server_manager
        self.command_manager = command_manager
        self.event_manager = event_manager
        self.event_manager.listen(MessageReceivedEvent, self.message_received_listener)
        self.event_manager.listen(ClientJoinServerEvent, self.client_join_listener)
        self.event_manager.listen(ClientDisconnectEvent, self.client_disconnect_listener)
        self.event_manager.listen(ServerStopEvent, self.server_stop_listener)
        self.event_manager.listen(GroupCreateEvent, self.group_create_listener)
        self.event_manager.listen(ClientLeaveGroupEvent, self.client_leave_group_listener)
        self.event_manager.listen(ClientChangeActiveGroupEvent, self.client_change_active_group_listener)
    
    
    async def message_received_listener(self, event: MessageReceivedEvent) -> None:
        client = event.client
        event_msg: Message = event.message
        self.logger.debug(f"Received message: {event_msg}")
        
        if type(event_msg) == ClientMessage:
            await client.active_group.broadcast(
                ClientMessage(client.username, client.privilege.value, event_msg.content),
                validators.exclude_client(client)
            )
        elif type(event_msg) == CommandMessage:
            client_privilege = client.privilege
            await self.command_manager.execute_command(client, client_privilege, event_msg)

    async def client_join_listener(self, event: ClientJoinServerEvent) -> None:
        client = event.client
        self.server_manager.add_client(client)
        await self.server_manager.broadcast(JoinMessage(
            client.username, client.privilege.value), validators.exclude_client(event.client))

    async def client_disconnect_listener(self, event: ClientDisconnectEvent) -> None:
        await self.server_manager.remove_client(event.client)
        await self.server_manager.broadcast(LeaveMessage(
            event.client.username), validators.exclude_client(event.client))
        self.logger.debug("Client {event.client.username} disconnected")

    async def server_stop_listener(self, event: ServerStopEvent) -> None:
        await self.server_manager.broadcast(DisconnectMessage())
        await self.server_manager.stop()

    async def group_create_listener(self, event: GroupCreateEvent) -> None:
        group = event.group
        await self.server_manager.add_group(group)

    async def client_leave_group_listener(self, event: ClientLeaveGroupEvent):
        client = event.client
        group = event.group
        client.groups.remove(group)
        group.remove_client(client)
        if client.active_group == group:
            client.active_group = self.server_manager.global_group

    async def client_change_active_group_listener(self, event: ClientChangeActiveGroupEvent):
        client = event.client
        active_group = client.active_group
        new_group = event.group
        if active_group:
            active_group.make_client_inactive(client)
        new_group.add_active_client(client)
        client.active_group = new_group
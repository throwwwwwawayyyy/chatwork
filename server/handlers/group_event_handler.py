import logging
from managers.event_manager import EventManager
from objects.messages import ClientMessage, JoinMessage, LeaveMessage, CommandMessage, DisconnectMessage, Message
from utils import validators
from objects.events import MessageReceivedEvent, ClientJoinServerEvent, ClientDisconnectEvent, ServerStopEvent
from managers.command_manager import CommandManager
from managers.client_manager import ClientManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.server_manager import ServerManager

class GroupEventHandler:
    def __init__(self, event_manager: EventManager, server_manager: 'ServerManager') -> None:
        self.logger = logging.getLogger(__name__)
        self.server_manager = server_manager
        self.event_manager = event_manager
        self.event_manager.listen(MessageReceivedEvent, self.message_received_listener)
        self.event_manager.listen(ClientJoinServerEvent, self.client_join_listener)
        self.event_manager.listen(ClientDisconnectEvent, self.client_disconnect_listener)
        self.event_manager.listen(ServerStopEvent, self.server_stop_listener)
    
    
    async def message_received_listener(self, event: MessageReceivedEvent) -> None:
        client: ClientManager = event.client
        event_msg: Message = event.message
        self.logger.debug(f"Received message: {event_msg}")
        
        if type(event_msg) == ClientMessage:
            await self.server_manager.broadcast(
                ClientMessage(client.username, client.privilege.value, event_msg.content),
                validators.exclude_client(client)
            )
        # elif type(event_msg) == CommandMessage:
        #     client_privilege = client.privilege
        #     await super().execute_command(client, client_privilege, event_msg)

    async def client_join_listener(self, event: ClientJoinServerEvent) -> None:
        client: ClientManager = event.client
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
from managers.event_manager import EventManager
from objects.messages import ClientMessage, JoinMessage, LeaveMessage, CommandMessage, DisconnectMessage, Message
from utils import validators
from objects.events import MessageReceivedEvent, ClientJoinEvent, ClientDisconnectEvent, ServerStopEvent
from managers.command_manager import CommandManager
from managers.client_manager import ClientManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.server_manager import ServerManager

class ServerHandler(CommandManager, EventManager):
    def __init__(self) -> None:
        super().__init__()
        super().listen(MessageReceivedEvent, self.message_received_listener)
        super().listen(ClientJoinEvent, self.client_join_listener)
        super().listen(ClientDisconnectEvent, self.client_disconnect_listener)
        super().listen(ServerStopEvent, self.server_stop_listener)
    
    
    async def message_received_listener(self: "ServerManager", event: MessageReceivedEvent) -> None:
        client: ClientManager = event.client
        event_msg: Message = event.message
        self.logger.debug(f"Received message: {event_msg}")
        
        if type(event_msg) == ClientMessage:
            await self.broadcast(
                ClientMessage(client.username, client.privilege.value, event_msg.content),
                validators.exclude_client(client)
            )
        elif type(event_msg) == CommandMessage:
            client_privilege = client.privilege
            await super().execute_command(client, client_privilege, event_msg)

    async def client_join_listener(self: "ServerManager", event: ClientJoinEvent) -> None:
        client: ClientManager = event.client
        self.add_client(client)
        await self.broadcast(JoinMessage(
            client.username, client.privilege.value), validators.exclude_client(event.client))

    async def client_disconnect_listener(self: "ServerManager", event: ClientDisconnectEvent) -> None:
        await self.remove_client(event.client)
        await self.broadcast(LeaveMessage(
            event.client.username), validators.exclude_client(event.client))
        self.logger.debug("Client {event.client.username} disconnected")

    async def server_stop_listener(self: "ServerManager", event: ServerStopEvent) -> None:
        await self.broadcast(DisconnectMessage())
        await self.stop()
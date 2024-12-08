import sys
from managers.event_manager import EventManager
from objects.messages import ClientMessage, JoinMessage, LeaveMessage, CommandMessage
from utils import validators
from objects.events import *
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
        super().listen(ClientLeaveEvent, self.client_leave_listener)
        super().listen(ServerStopEvent, self.server_stop_listener)
    
    
    async def message_received_listener(self: "ServerManager", event: MessageReceivedEvent) -> None:
        self.logger.debug(f"Received message: {event.message}")
        if type(event.message) in (ClientMessage, JoinMessage, LeaveMessage):
            try:
                await self.broadcast(
                    event.message,
                    validators.exclude_client(event.client)
                )
            except Exception as e:
                self.logger.exception(e)
        elif type(event.message) == CommandMessage:
            super().execute_command(event.message)

    async def client_join_listener(self: "ServerManager", event: ClientJoinEvent) -> None:
        client: ClientManager = event.client
        self.clients.append(client)
        self.usernames.append(client.username)
        await self.broadcast(JoinMessage(
            client.username, client.privilege), validators.exclude_client(event.client))

    async def client_leave_listener(self: "ServerManager", event: ClientLeaveEvent) -> None:
        self.logger.debug("Client {event.client.username} disconnected")
        self.clients.remove(event.client)
        await self.broadcast(LeaveMessage(
            event.client.username), validators.exclude_client(event.client))

    async def server_stop_listener(self: "ServerManager", event: ServerStopEvent) -> None:
        self.logger.debug("Server has been stopped")
        await self.stop()
        sys.exit(0)
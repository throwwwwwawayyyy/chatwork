from typing import Callable
from utils.event_handler import EventHandler
from objects.events import ClientJoinAttemptEvent, ClientJoinEvent, ClientLeaveEvent, MessageReceivedEvent
from objects.messages import JoinMessage, LeaveMessage
import utils.validators as validators
import logging

listeners: list[tuple] = []

class ServerHandlers:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        for listener in listeners:
            instantiated_listener = self.instantiate_listener(listener[1])
            EventHandler.listen(listener[0], instantiated_listener)

    def instantiate_listener(self, handler: Callable):
        async def wrapper(event):
            await handler(self, event)
        return wrapper

    @staticmethod
    def _add_handler(event_type):
        def wrapper(listener):
            listeners.append((event_type, listener))
        return wrapper
    
    @_add_handler(MessageReceivedEvent)
    async def message_received_handler(self, event: MessageReceivedEvent) -> None:
        self.logger.debug(f"Received message: {event.message}")
        try:
            await self.broadcast(
                event.message,
                validators.exclude_client(event.client)
            )
        except Exception as e:
            self.logger.exception(e)

    @_add_handler(ClientJoinAttemptEvent)
    async def client_join_attempt_handler(self, event: ClientJoinAttemptEvent) -> None:
        client = event.client
        is_ip_taken = client.ip in self.clients
        is_username_taken = client.username in self.usernames

        if is_ip_taken or is_username_taken:
            client.disconnect()

    @_add_handler(ClientJoinEvent)
    async def client_join_handler(self, event: ClientJoinEvent) -> None:
        client = event.client
        self.clients.append(client)
        self.usernames.append(client.username)
        await self.broadcast(JoinMessage(
            client.username, client.privilege), validators.exclude_client(event.client))

    @_add_handler(ClientLeaveEvent)
    async def client_leave_handler(self, event: ClientLeaveEvent) -> None:
        self.logger.debug("Client {event.client.username} disconnected")
        self.clients.remove(event.client)
        await self.broadcast(LeaveMessage(
            event.client.username), validators.exclude_client(event.client))
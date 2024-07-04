from typing import Callable
from utils.event_handler import EventHandler
from objects.events import ClientJoinAttemptEvent, ClientJoinEvent, ClientLeaveEvent, MessageReceiveEvent
from objects.messages import JoinMessage, LeaveMessage
import utils.validators as validators

listeners: list[tuple] = []

class ServerHandlers:

    def __init__(self) -> None:
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
    
    @_add_handler(MessageReceiveEvent)
    async def message_receive_handler(self, event: MessageReceiveEvent) -> None:
        print(event.message, end='\n\n')
        try:
            await self.broadcast(
                event.message,
                validators.exclude_client(event.client)
                )
        except Exception as e:
            print(e)

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
        print("Client disconnected")
        client = event.client
        self.clients.remove(client)
        await self.broadcast(LeaveMessage(
            client.username), validators.exclude_client(event.client))
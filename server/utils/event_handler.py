from objects.events import *
from objects.messages import *
from typing import Callable


class EventHandler:
    _listeners: dict[object, list] = {}
    
    @staticmethod
    def listen(event_type, listener) -> None:
        if event_type not in EventHandler._listeners:
            EventHandler._listeners[event_type] = []
        EventHandler._listeners[event_type].append(listener)

    async def fire(self, event) -> None:
        for listener in EventHandler._listeners[type(event)]:
            await listener(event)
            

class ServerHandlers:
    _listeners: list[tuple] = {}

    @staticmethod
    def _add_handler(event_type):
        def wrapper(listener):
            ServerHandlers._listeners.append((event_type, listener))
        return wrapper
    
    def __init__(self) -> None:
        for listener in self._listeners:
            instantiated_listener = self.instantiate_listener(listener[1])
            EventHandler.listen(listener[0], instantiated_listener)
    
    def instantiate_listener(self, handler: Callable):
        def wrapper(event):
            handler(self, event)
        return wrapper
    
    @_add_handler
    async def message_receive_handler(self, event: MessageReceiveEvent) -> None:
        print(event.message, end='\n\n')
        await self.broadcast(
            event.message,
            [event.author.ip])

    @_add_handler
    async def client_join_handler(self, event: ClientJoinEvent) -> None:
        client = event.client
        self.clients[client.ip] = client
        self.usernames.append(client.username)
        await self.broadcast(JoinMessage(
            client.username, client.privilage), [client.ip])

    @_add_handler
    async def client_leave_handler(self, event: ClientLeaveEvent) -> None:
        print("Client disconnected")
        client = event.client
        self.clients.pop(client.ip)
        await self.broadcast(LeaveMessage(
            client.username), [client.ip])

    @_add_handler
    async def client_join_attempt_handler(self, event: ClientJoinAttemptEvent) -> None:
        client = event.client
        is_ip_taken = client.ip in self.clients
        is_username_taken = client.username in self.usernames

        if is_ip_taken or is_username_taken:
            client.disconnect()

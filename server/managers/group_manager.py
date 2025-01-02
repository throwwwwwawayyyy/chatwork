import logging
from managers.client_manager import ClientManager
from objects.messages import Message
from objects.events import GroupCloseEvent
from managers.event_manager import EventManager


class GroupManager:
    def __init__(self, name: str, event_manager: EventManager) -> None:
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.authorized_clients: list[ClientManager] = []
        self.active_clients: list[ClientManager] = []
        self.event_manager = event_manager

    def add_active_client(self, client: ClientManager):
        if client not in self.authorized_clients:
            self.authorized_clients.append(client)
        self.active_clients.append(client)

    def remove_client(self, client: ClientManager):
        if client in self.authorized_clients:
            self.authorized_clients.remove(client)
        self.make_client_inactive(client)
        if not self.authorized_clients:
            self.event_manager.fire(GroupCloseEvent(self))

    def make_client_inactive(self, client):
        if client in self.active_clients:
            self.active_clients.remove(client)

    async def broadcast(self, 
                        message: Message, 
                        *client_validators: tuple[callable]) -> None:
        self.logger.debug(f"Broadcasting message: {message} to clients: {self.active_clients}")
        for client in self.active_clients:
            is_valid = all([validator(client) for validator in client_validators])
            if is_valid:
                await client.send_message(message)

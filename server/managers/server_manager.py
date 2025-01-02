import asyncio
import logging
from managers.client_manager import ClientManager
from handlers.server_event_handler import ServerEventHandler
from handlers.server_command_handler import ServerCommandHandler
from objects.messages import AckMessage, AuthMessage, Message
from objects.events import ClientJoinServerEvent, GroupCreateEvent, ClientChangeActiveGroupEvent
from utils import validators
from utils.enums import AckCode, Privilege
from managers.event_manager import EventManager
from managers.encryption_manager import EncryptionManager
from managers.command_manager import CommandManager
from managers.group_manager import GroupManager
from utils import utils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.group_manager import GroupManager


class ServerManager:
    def __init__(self, event_manager: EventManager, 
                 encryption_manager: EncryptionManager,
                 command_manager: CommandManager) -> None:
        self.logger = logging.getLogger(__name__)
        self.server: asyncio.Server = None

        self.clients: list[ClientManager] = []
        self.usernames: list[str] = []

        self.groups: list[GroupManager] = []
        self.group_names: list[str] = []
        self.global_group: GroupManager = GroupManager('global', event_manager)

        self.tasks: set[asyncio.Task] = set()
        self.is_running = True

        self.event_manager = event_manager
        self.encryption_manager = encryption_manager
        self.server_handler = ServerEventHandler(event_manager, command_manager, self)
        self.command_handler = ServerCommandHandler(event_manager, command_manager, self)

    @staticmethod
    async def create(event_manager: EventManager,
                     encryption_manager: EncryptionManager,
                     command_manager: CommandManager,
                     ip: str,
                     port: int) -> 'ServerManager':
        obj = ServerManager(event_manager, encryption_manager, command_manager)
        await event_manager.fire(GroupCreateEvent(GroupManager('global', event_manager)))
        obj.server = await asyncio.start_server(obj.handle_client, ip, port)

        addresses = ', '.join(str(sock.getsockname()) for sock in obj.server.sockets)
        obj.logger.debug(f"Serving on {addresses}")

        await obj.run_server()

    async def run_server(self) -> None:
        while self.is_running:
            await asyncio.sleep(0.5)

    async def handle_client(self, 
                            reader: asyncio.StreamReader, 
                            writer: asyncio.StreamWriter) -> None:
        task = asyncio.create_task(self._handle_client_task(reader, writer))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def _handle_client_task(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        client = ClientManager(reader, writer, self.event_manager, self.encryption_manager)
        await client.init_keys()
        while self.is_running and client.is_connected:
            if await self.process_credentials(client):
                await self.event_manager.fire(ClientJoinServerEvent(client))
                await self.event_manager.fire(ClientChangeActiveGroupEvent(client, self.global_group))
                await client.start_client()

    async def process_credentials(self, client: ClientManager):
        while True:
            auth_message: AuthMessage|None = await client.read_message()
            
            if not isinstance(auth_message, AuthMessage):
                return False

            if validators.validate_user(auth_message.username, auth_message.password, self.usernames):
                await client.send_message(AckMessage(
                    AckCode.CREDENTIALS_ACCEPTED.value))
                break
            else:
                await client.send_message(AckMessage(
                    AckCode.CREDENTIALS_DENIED.value))
                return False
                
        await client.send_message(AckMessage(AckCode.CLIENT_AUTHORIZED.value))
        client.username = auth_message.username

        if client.username == "matmat18":
            client.privilege = Privilege.ROOT
        
        return True

    def add_client(self, client: ClientManager):
        self.clients.append(client)
        self.usernames.append(client.username)

    async def remove_client(self, client: ClientManager):
        await client.disconnect()
        if client in self.clients:
            self.clients.remove(client)
            self.usernames.remove(client.username)

    async def add_group(self, group: GroupManager):
        self.groups.append(group)
        self.group_names.append(group.name)

    async def remove_group(self, group: GroupManager):
        self.groups.remove(group)
        self.group_names.remove(group.name)

    async def broadcast(self, 
                        msg: Message, 
                        *group_validators: tuple[callable]) -> None:
        self.logger.debug(f"Broadcasting message: {msg} to groups: {self.groups}")
        for group in self.groups:
            is_valid = all([validator(group) for validator in group_validators])
            if is_valid:
                await group.broadcast(msg)

    async def stop(self):
        self.logger.debug("Stopping the server...")
        self.is_running = False

        for client in self.clients:
            await self.remove_client(client)

        self.server.close()
        await self.server.wait_closed()

        for task in self.tasks:
            task.cancel()


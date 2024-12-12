from managers.client_manager import ClientManager
from handlers.server_handler import ServerHandler
from handlers.command_handler import CommandHandler
from utils.enums import State
from objects.messages import AckMessage, AuthMessage, Message
from objects.events import ClientJoinEvent
from utils import validators
from utils.enums import AckCode, Privilege
import asyncio
import logging


class ServerManager(ServerHandler, CommandHandler):
    def __init__(self) -> None:
        ServerHandler.__init__(self)
        CommandHandler.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.server: asyncio.Server = None
        self.clients: list[ClientManager] = []
        self.usernames: list[str] = []
        self.tasks: set[asyncio.Task] = set()
        self.is_running = True

    @staticmethod
    async def create(ip: str, port: int) -> 'ServerManager':
        obj = ServerManager()
        obj.server = await asyncio.start_server(obj.handle_client, ip, port)

        addresses = ', '.join(str(sock.getsockname()) for sock in obj.server.sockets)
        obj.logger.debug(f"Serving on {addresses}")

        await obj.run_server()

    async def run_server(self) -> None:
        while self.is_running:
            await asyncio.sleep(0.5)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        task = asyncio.create_task(self._handle_client_task(reader, writer))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def _handle_client_task(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        client = ClientManager(reader, writer, State.AUTH)
        await client.init_keys()
        while self.is_running and client.is_connected:
            if await self.process_credentials(client):
                await super().fire(ClientJoinEvent(client))
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

    async def broadcast(self, 
                        message: Message, 
                        *client_validators: tuple[callable]) -> None:
        self.logger.debug(f"Broadcasting message: {message} to clients: {self.clients}")
        for client in self.clients:
            is_valid = all([validator(client) for validator in client_validators])
            if is_valid:
                await client.send_message(message)

    def add_client(self, client: ClientManager):
        self.clients.append(client)
        self.usernames.append(client.username)

    async def remove_client(self, client: ClientManager):
        await client.disconnect()
        if client in self.clients:
            self.clients.remove(client)
            self.usernames.remove(client.username)

    async def stop(self):
        self.logger.debug("Stopping the server...")
        self.is_running = False

        for client in self.clients:
            await self.remove_client(client)

        self.server.close()
        await self.server.wait_closed()

        for task in self.tasks:
            task.cancel()

    def find_client_by_username(self, username: str) -> ClientManager:
        for client in self.clients:
            if client.username == username:
                return client


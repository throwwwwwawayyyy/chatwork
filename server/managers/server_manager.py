from managers.client_manager import ClientManager
from utils.server_handlers import ServerHandlers
from utils.event_handler import EventHandler
from utils.constants import State
from objects.messages import *
from objects.events import *
import asyncio
import logging


class ServerManager(EventHandler, ServerHandlers):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.server: asyncio.Server = None
        self.clients: list[ClientManager] = []
        self.usernames: list[str] = []
    
    @staticmethod
    async def create(ip: str, port: int) -> None:
        obj = ServerManager()
        obj.server = await asyncio.start_server(obj.handle_client, ip, port)

        addresses = ', '.join(str(sock.getsockname())
                          for sock in obj.server.sockets)
        obj.logger.debug(f'Serving on {addresses}')

        async with obj.server:
            await obj.server.serve_forever()

    async def handle_client(self,
                            reader: asyncio.StreamReader,
                            writer: asyncio.StreamWriter) -> None:
        client = ClientManager(reader, writer, State.AUTH)
        await client.init_keys()
        if await client.process_credentials():
            await super().fire(
                ClientJoinEvent(client))
            await client.start_client()
        else:
            client.disconnect()

    async def broadcast(self, 
                        message: Message, 
                        *client_validators: tuple[callable]) -> None:
        self.logger.debug(f"Broadcasting message: {message} to clients: {self.clients}")
        for client in self.clients:
            is_valid = all([validator(client) for validator in client_validators])
            if is_valid:
                client.send_message(message)
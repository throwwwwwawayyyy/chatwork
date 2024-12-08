from managers.client_manager import ClientManager
from event_handlers.server_handler import ServerHandler
from utils.constants import State
from objects.messages import *
from objects.events import *
import asyncio
import logging


class ServerManager(ServerHandler):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.server: asyncio.Server = None
        self.clients: list[ClientManager] = []
        self.usernames: list[str] = []
        self.tasks: set[asyncio.Task] = set()

    @staticmethod
    async def create(ip: str, port: int) -> None:
        obj = ServerManager()
        obj.server = await asyncio.start_server(obj.handle_client, ip, port)

        addresses = ', '.join(str(sock.getsockname()) for sock in obj.server.sockets)
        obj.logger.debug(f'Serving on {addresses}')

        async with obj.server:
            await obj.server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        task = asyncio.create_task(self._handle_client_task(reader, writer))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def _handle_client_task(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        client = ClientManager(reader, writer, State.AUTH)
        await client.init_keys()
        if await client.process_credentials():
            await super().fire(ClientJoinEvent(client))
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

    async def stop(self):
        self.logger.debug("Stopping the server...")

        for client in self.clients:
            client.disconnect()

        self.server.close()
        await self.server.wait_closed()

        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

        self.logger.debug("Server stopped.")
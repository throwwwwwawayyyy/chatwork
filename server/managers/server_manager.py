import asyncio
from managers.client_manager import ClientManager
from utils.event_handler import EventHandler, ServerHandlers
from objects.messages import *
from objects.events import *


class ServerManager(EventHandler, ServerHandlers):
    def __init__(self) -> None:
        self.server: asyncio.Server = None
        self.clients: dict[str, ClientManager] = {}
        self.usernames: list[str] = []
    
    @staticmethod
    async def create(ip: str, port: int) -> None:
        obj = ServerManager()
        obj.server = await asyncio.start_server(obj.handle_client, ip, port)

        addrs = ', '.join(str(sock.getsockname())
                          for sock in obj.server.sockets)
        print(f'Serving on {addrs}')

        async with obj.server:
            await obj.server.serve_forever()

    async def handle_client(self,
                            reader: asyncio.StreamReader,
                            writer: asyncio.StreamWriter) -> None:
        client = ClientManager(reader, writer)
        await client.init_keys()
        if await client.process_credentials():
            await client.start_client()
        else:
            client.disconnect()

    async def broadcast(self, 
                        message: Message, 
                        exclude: list[str]) -> None:
        for client in self.clients.values():
            if client.ip not in exclude:
                client.send_message(message)
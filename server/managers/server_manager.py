import asyncio
from managers.client_manager import ClientManager
from utils.event_handler import EventHandler
from objects.messages import *
from objects.events import *


class ServerManager:
    async def create(self) -> None:
        self.server = await asyncio.start_server(self.handle_client, '127.0.0.1', 8642)
        self.clients: dict[str, ClientManager] = {}
        self.usernames: list[str] = []
        self.event_handler = EventHandler()
        await self.init_listeners()

        addrs = ', '.join(str(sock.getsockname())
                          for sock in self.server.sockets)
        print(f'Serving on {addrs}')

        async with self.server:
            await self.server.serve_forever()

    async def init_listeners(self):
        self.event_handler.listen(
            self.message_receive_handler,
            MessageReceiveEvent)

        self.event_handler.listen(
            self.client_join_handler,
            ClientJoinEvent)

        self.event_handler.listen(
            self.client_leave_handler,
            ClientLeaveEvent)
        
        self.event_handler.listen(
            self.client_join_attempt_handler,
            ClientJoinAttemptEvent)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client = ClientManager(reader, writer, self.event_handler)
        await client.start_client()

    async def broadcast(self, message: Message, exclude: list[str]):
        for client in self.clients.values():
            if client.ip not in exclude:
                client.send_message(message)

    async def message_receive_handler(self, event: MessageReceiveEvent):
        print(event.message, end='\n\n')
        await self.broadcast(
            event.message,
            [event.author.ip])

    async def client_join_handler(self, event: ClientJoinEvent):
        client: ClientManager = event.client
        self.clients[client.ip] = client
        self.usernames.append(client.username)
        await self.broadcast(JoinMessage(
            client.username, client.privilage), [client.ip])

    async def client_leave_handler(self, event: ClientLeaveEvent):
        client: ClientManager = event.client
        self.clients.pop(client.ip)
        await self.broadcast(LeaveMessage(
            client.username), [client.ip])

    async def client_join_attempt_handler(self, event: ClientJoinAttemptEvent):
        client: ClientManager = event.client
        is_ip_taken = client.ip in self.clients
        is_username_taken = client.username in self.usernames
        
        if is_ip_taken or is_username_taken:
            client.disconnect()
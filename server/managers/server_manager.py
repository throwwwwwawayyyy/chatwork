import asyncio
from managers.client_manager import Client
from utils.event_handler import EventHandler
from objects.messages import Message, JoinMessage
from objects.events import MessageReceivedEvent, UserJoinedEvent

class ServerManager:
    async def create(self) -> None:
        self.server = await asyncio.start_server(self.handle_client, '10.0.0.62', 8642)
        self.clients: dict[str, Client] = {}
        self.event_handler = EventHandler()
        
        self.event_handler.listen(
            lambda event: print(event.message.serialize()), 
            MessageReceivedEvent)
        
        self.event_handler.listen(
            lambda event: self.broadcast(JoinMessage(event.username, event.privilage)),
            UserJoinedEvent
        )

        addrs = ', '.join(str(sock.getsockname()) for sock in self.server.sockets)
        print(f'Serving on {addrs}')

        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client = Client(reader, writer, self.event_handler)
        self.clients[client.ip] = client
        await client.start_client()
        
    async def broadcast(self, message: Message, exclude: list[Client]):
        for client in self.clients.values():
            if client not in exclude:
                client.send_message(message)

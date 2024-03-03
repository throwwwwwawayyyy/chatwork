import asyncio
from utils.event_handler import EventHandler
from objects.events import MessageReceiveEvent, ClientJoinEvent, ClientLeaveEvent
from objects.messages import AckMessage, ClientMessage, Message
import utils.constants as constants
from utils.validators import validate_credentials


class ClientManager(EventHandler):
    def __init__(self,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
        self.reader = reader
        self.writer = writer
        self.ip, self.port = writer.get_extra_info('peername')
        self.username = None
        self.privilage = constants.Privileges.DEFAULT.value

        print(f"Connected from: ({self.ip}, {self.port})")

    async def start_client(self) -> None:
        await super().fire(
            ClientJoinEvent(self))

        while True:
            content = await self.read_message()
            
            if not content:
                break
            
            message = ClientMessage(self.username, content)
            await super().fire(MessageReceiveEvent(message, self))

        self.disconnect()
        return True

    async def process_credentials(self):
        while not is_credentials_valid:
            username = await self.read_message()
            password = await self.read_message()
            
            if not (username and password):
                return False
            
            is_credentials_valid = validate_credentials(username, password)

            if is_credentials_valid:
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_ACCEPTED))
                return True
            else:
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_DENIED))
                
        self.send_message(AckMessage(constants.AckCodes.CLIENT_AUTHORIZED))
        self.username = username.decode('utf-8')

    async def disconnect(self) -> None:
        self.writer.close()
        
    def send_message(self, message: Message):
        print(message.serialize())
        self.writer.write(message.serialize())
        
    async def read_message(self):
        try:
            return await self.reader.read(100)
        except ConnectionResetError:
            super().fire(ClientLeaveEvent)

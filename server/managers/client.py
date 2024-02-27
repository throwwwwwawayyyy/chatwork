import asyncio
from utils.event_handler import EventHandler
from objects.events import MessageReceivedEvent, UserJoinedEvent
from objects.messages import AckMessage, ClientMessage, Message
import utils.constants as constants


class Client:
    def __init__(self, 
                 reader: asyncio.StreamReader, 
                 writer: asyncio.StreamWriter, 
                 event_handler: EventHandler) -> None:
        self.reader = reader
        self.writer = writer
        self.event_handler = event_handler
        self.ip, self.port = writer.get_extra_info('peername')
        self.username = None
        self.privilage = "admin"
        
        print(f"Connected from: ({self.ip}, {self.port})")

    def send_message(self, message: Message):
        print(message.serialize())
        self.writer.write(message.serialize())

    async def start_client(self):
        await self.validate_credentials()
        
        self.event_handler.fire(UserJoinedEvent(self.username, self.privilage))
        
        while True:
            content = await self.reader.read(100)

            if not content:
                print(f"Closing connection with ({self.ip}, {self.port})")
                break

            message = ClientMessage(content, self.ip, self.port)
            self.event_handler.fire(MessageReceivedEvent(message))

        self.writer.close()
        
    async def validate_credentials(self):
        is_credentials_valid = False
        username = ''
        
        while not is_credentials_valid:
            username = await self.reader.read(100)
            password = await self.reader.read(100)
            
            if password == b'nignig123':
                self.send_message(AckMessage(constants.AckCodes.CREDENTIALS_ACCEPTED))
                is_credentials_valid = True
            else:
                self.send_message(AckMessage(constants.AckCodes.CREDENTIALS_DENIED))
        
        self.username = username
            
            
             

import asyncio
from utils.event_handler import EventHandler
from objects.events import MessageReceivedEvent, UserJoinedEvent
from objects.messages import AckMessage, ClientMessage, Message
import utils.constants as constants
from utils.validators import validate_username, validate_password


class ClientManager:
    def __init__(self,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter,
                 event_handler: EventHandler) -> None:
        self.reader = reader
        self.writer = writer
        self.event_handler = event_handler
        self.ip, self.port = writer.get_extra_info('peername')
        self.username = None
        self.privilage = constants.Privileges.DEFAULT.value

        print(f"Connected from: ({self.ip}, {self.port})")

    async def start_client(self):
        await self.validate_credentials()

        await self.event_handler.fire(
            UserJoinedEvent(self))

        while True:
            try:
                content = await self.read_message()
            except ConnectionResetError:
                print(f"Closing connection with ({self.ip}, {self.port})")
                break
            except Exception as e:
                print(e)
                break

            message = ClientMessage(self.username, content)
            await self.event_handler.fire(MessageReceivedEvent(message, self.ip))

        self.writer.close()

    async def validate_credentials(self):
        is_credentials_valid = False
        username = ''

        while not is_credentials_valid:
            username = await self.read_message()
            password = await self.read_message()

            if validate_username(username) and validate_password(password):
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_ACCEPTED))
                is_credentials_valid = True
            else:
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_DENIED))

        self.send_message(AckMessage(constants.AckCodes.CLIENT_AUTHORIZED))

        self.username = username.decode('utf-8')
        
    def send_message(self, message: Message):
        print(message.serialize())
        self.writer.write(message.serialize())
        
    async def read_message(self):
        return await self.reader.read(100)

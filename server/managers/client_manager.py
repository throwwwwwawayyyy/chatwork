import asyncio
from managers.encryption_manager import EncryptionManager
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
        self.encryptor = EncryptionManager()

        print(f"Connected from: ({self.ip}, {self.port})")
        
    async def init_keys(self):
        await self.encryptor.share_keys(self.reader, self.writer)

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
        while True:
            username = await self.read_message()
            password = await self.read_message()
            
            if not (username and password):
                return False

            if validate_credentials(username, password):
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_ACCEPTED))
                break
            else:
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_DENIED))
                
        self.send_message(AckMessage(constants.AckCodes.CLIENT_AUTHORIZED))
        self.username = username.decode('utf-8')
        
        return True

    async def disconnect(self) -> None:
        self.writer.close()
        
    def send_message(self, message: Message):
        raw_message = message.serialize()
        encrypted_raw_message = self.encryptor.encrypt(raw_message)
        
        print(raw_message)
        self.writer.write(encrypted_raw_message)
        
    async def read_message(self):
        try:
            encrypted_raw_message = await self.reader.read(200)
            raw_message = self.encryptor.decrypt(encrypted_raw_message)
            return raw_message
        except ConnectionResetError:
            super().fire(ClientLeaveEvent)

import asyncio
import logging
from managers.encryption_manager import EncryptionManager
from managers.event_manager import EventManager
from objects.events import MessageReceivedEvent, ClientJoinEvent, ClientLeaveEvent
from objects.messages import AckMessage, ClientMessage, Message, AuthMessage
import utils.constants as constants
from utils.validators import validate_credentials

class ClientManager(EventManager):
    def __init__(self,
                reader: asyncio.StreamReader,
                writer: asyncio.StreamWriter,
                state: constants.State) -> None:
        self.logger = logging.getLogger(__name__)
        self.reader = reader
        self.writer = writer
        self.state = state
        self.ip, self.port = writer.get_extra_info('peername')
        self.username = None
        self.privilege = constants.Privileges.DEFAULT.value
        self.encryption_manager = EncryptionManager()
        self.is_stopped = False

        self.logger.debug(f"Connected from: ({self.ip}, {self.port})")
        
    async def init_keys(self):
        await self.encryption_manager.share_keys(self.reader, self.writer)

    async def start_message_loop(self):
        while True:
            client_message: ClientMessage|None = await self.read_message()
            
            if not isinstance(client_message, ClientMessage) or self.is_stopped:
                break

            await super().fire(MessageReceivedEvent(client_message, self))

    async def start_client(self) -> None:
        self.logger.debug(f"Starting client")
        await self.start_message_loop()

    async def process_credentials(self):
        while True:
            auth_message: AuthMessage|None = await self.read_message()
            
            if not isinstance(auth_message, AuthMessage):
                return False

            if validate_credentials(auth_message):
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_ACCEPTED.value))
                break
            else:
                self.send_message(AckMessage(
                    constants.AckCodes.CREDENTIALS_DENIED.value))
                
        self.send_message(AckMessage(constants.AckCodes.CLIENT_AUTHORIZED.value))
        self.username = auth_message.username
        
        return True

    def disconnect(self) -> None:
        self.writer.close()
        self.is_stopped = True
        
    def send_message(self, message: Message):
        raw_message = message.serialize()
        encrypted_raw_message = self.encryption_manager.encrypt(raw_message)
        self.writer.write(encrypted_raw_message)
        
    async def read_message(self) -> Message:
        try:
            encrypted_raw_message = await self.reader.read(2048)
            raw_message = self.encryption_manager.decrypt(encrypted_raw_message)
            return Message.from_bytes(raw_message)
        except ConnectionResetError:
            await super().fire(ClientLeaveEvent(self))
            return None

import asyncio
import logging
from managers.encryption_manager import EncryptionManager
from managers.event_manager import EventManager
from objects.events import MessageReceivedEvent, ClientDisconnectEvent
from objects.messages import ClientMessage, Message
from utils.enums import Privilege
from rsa import DecryptionError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.group_manager import GroupManager


class ClientManager:
    def __init__(self,
                reader: asyncio.StreamReader,
                writer: asyncio.StreamWriter,
                event_manager: EventManager,
                encryption_manager: EncryptionManager) -> None:
        self.is_connected = True
        self.logger = logging.getLogger(__name__)
        self.reader = reader
        self.writer = writer
        self.ip, self.port = writer.get_extra_info('peername')
        self.username = None
        self.active_group: GroupManager = None
        self.groups: list[GroupManager] = []
        self.privilege = Privilege.DEFAULT
        self.event_manager = event_manager
        self.encryption_manager = encryption_manager


        self.logger.debug(f"Connected from: ({self.ip}, {self.port})")
        
    async def init_keys(self):
        await self.encryption_manager.share_keys(self.reader, self.writer)

    async def start_message_loop(self):
        while True:
            client_message: ClientMessage|None = await self.read_message()

            if not client_message:
                break

            await self.event_manager.fire(MessageReceivedEvent(client_message, self))

    async def start_client(self) -> None:
        self.logger.debug("Starting client")
        await self.start_message_loop()

    async def disconnect(self) -> None:
        self.writer.close()
        for group in self.groups:
            group.remove_client(self)
        self.is_connected = False
        
    async def send_message(self, message: Message):
        try:
            self.logger.debug(f"Sent message: {message}")
            raw_message = message.serialize()
            encrypted_raw_message = self.encryption_manager.encrypt(raw_message)
            self.writer.write(encrypted_raw_message)
        except ConnectionResetError:
            await self.event_manager.fire(ClientDisconnectEvent(self))
        
    async def read_message(self) -> Message:
        try:
            encrypted_raw_message = await self.reader.read(2048)
            raw_message = self.encryption_manager.decrypt(encrypted_raw_message)
            return Message.from_bytes(raw_message)
        except (DecryptionError, ConnectionResetError):
            await self.event_manager.fire(ClientDisconnectEvent(self))

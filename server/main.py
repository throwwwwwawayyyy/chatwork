import asyncio
import logging
import datetime
from dashboard import dashboard
from managers.server_manager import ServerManager
from utils.config import NetworkConfig, EncryptionConfig
from managers.event_manager import EventManager
from managers.encryption_manager import EncryptionManager
from managers.command_manager import CommandManager
from managers.group_manager import GroupManager

time_log = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
logging.basicConfig(filename=f"server//logs//debug_{time_log}.log", level=logging.DEBUG, filemode="w+")

async def main() -> None:
    network_config = NetworkConfig()
    encryption_config = EncryptionConfig()
    event_manager = EventManager()
    encryption_manager = EncryptionManager(encryption_config.rsa_key_default_size)
    command_manager = CommandManager()
    global_group = GroupManager("global", event_manager)

    dashboard.start_dashboard(command_manager)

    await ServerManager.create(event_manager, 
                               encryption_manager,
                               command_manager, 
                               network_config.ip, 
                               network_config.port)


if __name__ == "__main__":
    asyncio.run(main())

from managers.server_manager import ServerManager
from managers.config_manager import NetworkConfig
import asyncio

async def main() -> None:
    network_config = NetworkConfig()
    await ServerManager.create(network_config.ip, network_config.port)


if __name__ == "__main__":
    asyncio.run(main())
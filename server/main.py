# from dashboard import dashboard
from managers.server_manager import ServerManager
from managers.config_manager import NetworkConfig
import asyncio
import logging
import datetime

time_log = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
logging.basicConfig(filename=f"server//logs//debug_{time_log}.log", level=logging.DEBUG, filemode="w+")

async def main() -> None:
    network_config = NetworkConfig()
    await ServerManager.create(network_config.ip, network_config.port)


if __name__ == "__main__":
    # dashboard.start_dashboard()
    asyncio.run(main())
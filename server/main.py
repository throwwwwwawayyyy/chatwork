from managers.server_manager import ServerManager
import asyncio
import logging


async def main():
    await ServerManager().create()


if __name__ == "__main__":
    asyncio.run(main())
from managers.server_manager import ServerManager
import asyncio

async def main() -> None:
    await ServerManager.create()


if __name__ == "__main__":
    asyncio.run(main())
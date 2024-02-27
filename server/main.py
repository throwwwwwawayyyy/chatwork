from server import Server
import asyncio


async def main():
    await Server().create()


if __name__ == "__main__":
    asyncio.run(main())
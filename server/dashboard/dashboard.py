import threading
import asyncio
from objects.messages import CommandMessage, Message
from utils.enums import Privilege
from handlers.command_handler import CommandHandler


class Dashboard(CommandHandler):
    def __init__(self):
        self.is_stopped = False

    async def main_loop(self):
        content = ''
        while not self.is_stopped:
            content = input("Command: ").split(' ')
            cmd_name = content[0]
            args = []

            if len(content) > 1:
                args = content[1:len(content)]

            cmd_message = CommandMessage(cmd_name=cmd_name, args=args)
            await super().execute_command(RootSender(), Privilege.ROOT, cmd_message)

            self.is_stopped = cmd_name == "stop"


class RootSender:
    privilege = Privilege.ROOT

    async def send_message(self, msg: Message):
        try:
            print(msg.content)
        except AttributeError:
            print(msg)


def start_dashboard():
    dashboard = Dashboard()
    _thread = threading.Thread(target=asyncio.run, args=(dashboard.main_loop(),))
    _thread.start()

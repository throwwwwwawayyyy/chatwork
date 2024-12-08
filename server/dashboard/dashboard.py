import threading
import asyncio
from objects.messages import CommandMessage
from command_handlers.admin_commands_handler import AdminCommandsHandler


class Dashboard(AdminCommandsHandler):
    def __init__(self):
        super().__init__()
        self.is_stopped = False

    async def main_loop(self):
        content = ''
        while not self.is_stopped:
            content = input("Command: ").split()
            cmd_name = content[0]
            args = []

            if len(content) > 1:
                args = content[1:-1]

            cmd_message = CommandMessage(cmd_name=cmd_name, args=args)
            await super().execute_command(cmd_message)

            if cmd_name == "stop":
                break


def start_dashboard():
    dashboard = Dashboard()
    _thread = threading.Thread(target=asyncio.run, args=(dashboard.main_loop(),))
    _thread.start()

import logging
from objects.messages import CommandMessage

class CommandManager():
    commands: dict[str, callable] = {}

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def register_command(self, cmd_name, cmd_callback):
        self.logger.debug(f"Registered command: {cmd_name}")
        self.commands[cmd_name] = cmd_callback

    async def execute_command(self, cmd_message: CommandMessage) -> bool:
        self.logger.debug(f"Executed command: {cmd_message.cmd_name}")
        cmd_name = cmd_message.cmd_name
        args = cmd_message.args

        if cmd_name in self.commands:
            await self.commands[cmd_name](*args)
            return True
        return False

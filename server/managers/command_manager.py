import logging
from objects.messages import CommandMessage, AckMessage
from utils.enums import Privilege, AckCode
from managers.client_manager import ClientManager
from typing import Callable

class CommandManager:
    commands: dict[str, tuple[Callable, Privilege]] = {}

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def register_command(self, cmd_name: str, cmd_callback: Callable, privilege: Privilege):
        self.logger.debug(f"Registered command: {cmd_name}")
        self.commands[cmd_name] = (cmd_callback, privilege)

    async def execute_command(self, sender: ClientManager, sender_priv: Privilege, cmd_message: CommandMessage):
        cmd_name = cmd_message.cmd_name
        args = cmd_message.args

        command_success = False

        cmd = self.commands.get(cmd_name)

        if cmd:
            cmd_callback = cmd[0]
            cmd_priv = cmd[1]
            if self._check_privilege(cmd_priv, sender_priv):
                try:
                    command_success = await cmd_callback(sender, *args)
                    self.logger.debug(f"Executed command: {cmd_message.cmd_name}")
                except ValueError:
                    self.logger.debug(f"Command encountered a ValueError (probably wrong args): {cmd_name}")
        
        if command_success:
            await sender.send_message(AckMessage(AckCode.COMMAND_SUCCESS.value))
        else:
            await sender.send_message(AckMessage(AckCode.COMMAND_FAIL.value))

    
    def _check_privilege(self, cmd_priv: Privilege, sender_priv: Privilege):
        return sender_priv.value >= cmd_priv.value

import subprocess
from managers.command_manager import CommandManager
from managers.event_manager import EventManager
from objects.events import ServerStopEvent
from objects.messages import SystemMessage
from utils.enums import Privilege
from managers.client_manager import ClientManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from managers.server_manager import ServerManager

class CommandHandler(CommandManager, EventManager):
    def __init__(self) -> None:
        super().__init__()
        super().register_command("help", self.help_command, Privilege.DEFAULT)
        super().register_command("stop", self.stop_command, Privilege.ROOT)
        super().register_command("announce", self.announce_command, Privilege.ROOT)
        super().register_command("say", self.say_command, Privilege.ROOT)
        super().register_command("bash", self.bash_command, Privilege.ROOT)
        super().register_command("promote", self.promote_command, Privilege.ADMIN)

    async def help_command(self: 'ServerManager', sender: ClientManager) -> bool:
        """Shows this message."""
        cmd_list = super().commands
        cmd_name_list = [cmd for cmd in cmd_list.keys()]

        help_text = 'Available commands:'

        for cmd_name in cmd_name_list:
            cmd_priv = cmd_list[cmd_name][1]
            cmd_doc = cmd_list[cmd_name][0].__doc__

            if cmd_doc.startswith('*') and not sender.privilege == Privilege.ROOT: 
                continue

            help_text += f"\n{cmd_name} [{cmd_priv.name}]: {cmd_doc}"

        await sender.send_message(SystemMessage(help_text))
        return True

    async def stop_command(self, sender) -> bool:
        """*Stops the server"""
        await super().fire(ServerStopEvent())
        return True
    
    async def announce_command(self: 'ServerManager', sender, *text) -> bool:
        """*Announces something"""
        await self.broadcast(SystemMessage(' '.join(text)))
        return True
    
    async def say_command(self: 'ServerManager', sender, username, *text) -> bool:
        """*Says something"""
        recipient = self.find_client_by_username(username)
        await recipient.send_message(SystemMessage(' '.join(text)))
        return True
    
    async def bash_command(self: 'ServerManager', sender: ClientManager, username, *text) -> bool:
        """*Execute shell command"""
        proc = subprocess.Popen("ifconfig", stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        sender.send_message(SystemMessage(out))
        return True

    async def promote_command(self: 'ServerManager', sender, username: str) -> bool:
        """Promotes anyone below you"""
        client: ClientManager = self.find_client_by_username(username)
        client_priv = client.privilege
        sender_priv = sender.privilege
        if sender_priv.value - client_priv.value > 1:
            client.privilege = Privilege(client_priv.value + 1)
            return True
        return False
        
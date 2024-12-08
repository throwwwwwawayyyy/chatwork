from managers.command_manager import CommandManager
from managers.event_manager import EventManager
from objects.events import ServerStopEvent

class AdminCommandsHandler(CommandManager, EventManager):
    def __init__(self) -> None:
        super().__init__()
        super().register_command("stop", self.stop)

    async def stop(self):
        await super().fire(ServerStopEvent())
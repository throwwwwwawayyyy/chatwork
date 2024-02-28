from objects.events import *


class EventHandler:
    def __init__(self) -> None:
        self.listeners: dict[object, list] = {}

    def listen(self, listener, event_type):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    async def fire(self, event):
        for listener in self.listeners[type(event)]:
            await listener(event)

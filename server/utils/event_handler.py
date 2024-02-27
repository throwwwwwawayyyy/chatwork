from objects.events import MessageReceivedEvent, UserJoinedEvent


class EventHandler:
    def __init__(self) -> None:
        self.listeners: dict[object, list] = {
            MessageReceivedEvent: [],
            UserJoinedEvent: []
        }

    def listen(self, listener, event_type):
        self.listeners[event_type].append(listener)

    async def fire(self, event):
        for listener in self.listeners[type(event)]:
            await listener(event)

import logging

class EventManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.listeners: dict = {}
    
    def listen(self, event_type, listener) -> None:
        self.logger.debug(f"Listening to: {event_type}")
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    async def fire(self, event) -> None:
        self.logger.debug(f"Event fired: {event}")
        try:
            for listener in self.listeners[type(event)]:
                await listener(event)
        except Exception as e:
            self.logger.error(e)
import logging

logger = logging.getLogger(__name__)

class EventManager:
    listeners: dict = {}
    
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def listen(event_type, listener) -> None:
        logger.debug(f"Listening to: {event_type}")
        if event_type not in EventManager.listeners:
            EventManager.listeners[event_type] = []
        EventManager.listeners[event_type].append(listener)

    async def fire(self, event) -> None:
        logger.debug(f"Event fired: {event}")
        try:
            for listener in EventManager.listeners[type(event)]:
                await listener(event)
        except Exception as e:
            logger.error(e)
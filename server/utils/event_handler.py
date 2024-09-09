import logging

logger = logging.getLogger(__name__)

class EventHandler:
    listeners: dict[object, list] = {}
    
    @staticmethod
    def listen(event_type, listener) -> None:
        logger.debug(f"Listening to: {event_type}")
        if event_type not in EventHandler.listeners:
            EventHandler.listeners[event_type] = []
        EventHandler.listeners[event_type].append(listener)

    async def fire(self, event) -> None:
        try:
            for listener in EventHandler.listeners[type(event)]:
                await listener(event)
        except Exception as e:
            logger.error(e)
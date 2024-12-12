import logging

class EventManager:
    logger = logging.getLogger(__name__)
    listeners: dict = {}
    
    def listen(self, event_type, listener) -> None:
        EventManager.logger.debug(f"Listening to: {event_type}")
        if event_type not in EventManager.listeners:
            EventManager.listeners[event_type] = []
        EventManager.listeners[event_type].append(listener)

    async def fire(self, event) -> None:
        EventManager.logger.debug(f"Event fired: {event}")
        try:
            for listener in EventManager.listeners[type(event)]:
                await listener(event)
        except Exception as e:
            EventManager.logger.error(e)
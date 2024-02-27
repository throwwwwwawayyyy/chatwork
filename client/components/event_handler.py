class EventHandler:
    _listeners: dict

    def __init__(self):
        self._listeners = {}

    def add_listener(self, event_name: str, callback):
        if event_name in self._listeners:
            self._listeners[event_name].append(callback)
        else:
            self._listeners[event_name] = [callback]

    def remove_listener(self, event_name: str):
        if event_name in self._listeners:
            self._listeners[event_name].pop()

    def trigger_event(self, event_name: str, *args, **kwargs):
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                callback(*args, **kwargs)
import uuid

class Connection:
    def __init__(self, event, connection_id):
        self._event = event
        self._id = connection_id
        self.connected = True

    def Disconnect(self):
        if self.connected and self._event:
            if self._id in self._event.Listeners:
                del self._event.Listeners[self._id]
            self._event = None
            self._id = None
            self.connected = False

class Signal:
    def __init__(self):
        self.Listeners: dict[str, function] = {}

    # @staticmethod 
    def new(self):
        return Signal()

    def Connect(self, func: function):
        connection_id = uuid.uuid4()
        self.Listeners[connection_id] = func
        return Connection(self, connection_id)

    def Fire(self, *args):
        for func in list(self.Listeners.values()):
            func(*args)
import uuid

class Connection:
    def __init__(self, event, connection_id):
        self._event = event
        self._id = connection_id
        self.connected = True

    def Disconnect(self):
        if self.connected and self._event:
            # Remove this specific connection from the dictionary
            if self._id in self._event.Listeners:
                del self._event.Listeners[self._id]
            
            # Wipe references for Garbage Collection
            self._event = None
            self._id = None
            self.connected = False
            self = None

class Event:
    def new(self):
        self = Event.new()
        self.Listeners = {}
        return self

    def Connect(self, func):
        connection_id = uuid.uuid4()
        self.Listeners[connection_id] = func
        
        return Connection(self, connection_id)

    def Fire(self, *args):
        for func in list(self.Listeners.values()):
            func(*args)

class Signal:
    def new(self):
        return Event(self)
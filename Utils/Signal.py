class Connection:
    def __init__(self, event, func):
        self.event = event
        self.func = func
        self.connected = True

    def Disconnect(self):
        if self.func in self.event.Listeners:
            del self.event.Listeners[self.func]
            self.connected = False
        
        self = None

class Event:
    def __init__(self):
        self.Listeners = {}

    def Connect(self, func):
        self.Listeners[func] = func
        return Connection(self, func)

    def Fire(self, *args):
        for func in list(self.Listeners.values()):
            func(*args)
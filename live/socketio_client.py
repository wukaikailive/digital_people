import socketio


class SocketioClient:
    client: socketio.Client
    server: str
    port: int

    def __init__(self, server, port):
        self.server = server
        self.port = port

    def connect(self):
        self.client = socketio.Client()
        self.client.connect(f"{self.server}:{self.port}")

    def disconnect(self):
        if self.client.connected:
            self.client.disconnect()

    def send_data(self, event, data):
        self.client.emit(event, data)

    def send(self, msg):
        pass

    def on(self, event, handler=None, namespace=None):
        self.client.on(event, handler, namespace)
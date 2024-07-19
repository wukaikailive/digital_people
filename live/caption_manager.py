"""
发送字幕
"""
import time

import socketio


class CaptionManager:
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

    def send(self, msg):
        self.client.emit("cmd", {"name": "caption", "text": msg})


if __name__ == "__main__":
    caption_manager = CaptionManager("http://127.0.0.1", 8082)
    caption_manager.connect()
    time.sleep(1)
    caption_manager.send("深刻觉得还是看到后")
    time.sleep(1)
    caption_manager.disconnect()
    print("disconnected")

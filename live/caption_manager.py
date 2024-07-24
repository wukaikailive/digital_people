"""
发送字幕
"""
import time

from live.socketio_client import SocketioClient


class CaptionManager(SocketioClient):
    def send(self, msg):
        self.send_data("cmd", {"name": "caption", "text": msg})


if __name__ == "__main__":
    caption_manager = CaptionManager("http://127.0.0.1", 8082)
    caption_manager.connect()
    time.sleep(1)
    caption_manager.send("深刻觉得还是看到后")
    time.sleep(1)
    caption_manager.disconnect()
    print("disconnected")

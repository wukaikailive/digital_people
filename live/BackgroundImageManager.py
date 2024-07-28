"""
发送背景图，暂时用发送弹幕功能代替，此文件暂时不启用
"""
import time

from live.SocketioClient import SocketioClient


class BackgroundImageManager(SocketioClient):
    def send(self, msg):
        self.send_data("cmd", {"name": "background_image", "text": msg})


if __name__ == "__main__":
    manager = BackgroundImageManager("http://127.0.0.1", 8082)
    manager.connect()
    time.sleep(1)
    manager.send("C:/Users/wukai/Downloads/1-图书推荐-5.png")
    time.sleep(1)
    manager.disconnect()
    print("disconnected")


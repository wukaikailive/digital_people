import logging
import os
from multiprocessing import Process

from barrage import barrage_server
from live.SocketioClient import SocketioClient

logger = logging.getLogger(__name__)


class BarrageManager(SocketioClient):

    __barrage_thread: Process = None

    barrages: list = []

    def on_receive_user_barrage(self, barrage):
        self.barrages.append(barrage)

    def clear(self):
        self.barrages.clear()

    def has_barrage(self):
        return len(self.barrages) > 0

    def connect(self):
        # 连接通讯服务
        super().connect()
        # 打开弹幕监听服务
        self.on_barrage_listing()
        self.on("receive_user_barrage", self.on_receive_user_barrage)

    def disconnect(self):
        super().disconnect()
        # 关闭弹幕监听服务
        self.off_barrage_listing()

    def on_barrage_listing(self):
        logger.info("启动弹幕服务")
        self.__barrage_thread = Process(target=barrage_server.start)
        self.__barrage_thread.start()

    def off_barrage_listing(self):
        if self.__barrage_thread.is_alive():
            self.__barrage_thread.terminate()

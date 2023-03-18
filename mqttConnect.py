# mqttConnect
import gc
from umqtt.simple import MQTTClient
import utime
from utils import wifi, connectWIFI
# 兼容性导入
try:
    import uasyncio
except ImportError:
    import asyncio as uasyncio

# 回收垃圾
gc.collect()


class MQTT(MQTTClient):
    """操作 MQTT 服务"""

    def __init__(self, client_id, server, port=0, user=None, password=None, keeyalive=30, ssl=False, ssl_params=None, *arg, **kw):
        super().__init__(client_id, server, port, user,
                         password, keeyalive, ssl, ssl_params, *arg, **kw)

        self.content = '{"timestamp":%s,"data":%s}'

    @property
    def timestamp():
        return utime.time()

    async def sub(self, topic, callback):
        """订阅主题并保持连接
        eCallback 发生错误时的回调
        """
        a = 0
        isNeedConnect = True  # 是否需要连接

        while True:
            try:
                if isNeedConnect:
                    print("connecting mqtt......")
                    self.connect()
                    isNeedConnect = False

                a += 1
                print(f"Keepconnect {a}")
                self.set_callback(callback)  # 设置回调
                self.subscribe(b'%s' % topic)  # 设置订阅
                self.check_msg()  # 非堵塞检查
            except Exception as e:
                print(f"[ERROR] Reconnect Now!{e}")
                if not wifi.isconnected():
                    connectWIFI()
                # 设置重连
                isNeedConnect = True

            await uasyncio.sleep(1)  # 异步休息

    def syncPub(self, topic: str, msg: str, retries=3, *args, **kw):
        """同步发布连接"""
        content = self.content % (self.timestamp, msg)

        for _ in range(retries):
            try:
                print(f"send {topic} {content}")
                self.publish(topic, content, *args, **kw)
                return
            except Exception as e:
                print(f"[Error]send err:{e}")
                continue


if __name__ == "__main__":
    pass

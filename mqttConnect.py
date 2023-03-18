# mqttConnect
import gc
from umqtt.simple import MQTTClient
import utime
# 兼容性导入
try:
    import uasyncio
except ImportError:
    import asyncio as uasyncio

# 启动垃圾回收器
gc.collect()


# mqtts://broker.diandeng.tech:1883 电灯科技

### Config ####
blinker_tk = "335562d5d103"
mserver = "broker-cn.emqx.io"
port = "1883"

client_id = "mqttx_b6b02f04"  # 可选
user = None
password = None
###############


class MQTT(MQTTClient):
    """操作 MQTT 服务"""

    def __init__(self, client_id, server, port=0, user=None, password=None, keeyalive=30, ssl=False, ssl_params=None, *arg, **kw):
        super().__init__(client_id, server, port, user,
                         password, keeyalive, ssl, ssl_params, *arg, **kw)

        self.content = '{"timestamp":%s,"data":%s}'

    @property
    def timestamp():
        return utime.time()

    def cb(self, topic, msg):
        """接受订阅源传来信息的回调函数
        留空,调用时再重写此方法
        """
        pass

    async def subs(self, *subs: str, eCallback: function = None):
        """订阅主题并保持连接
        eCallback 发生错误时的回调
        """
        self.set_callback(self.cb)  # 设置总回调.只能有一个总回调方法
        self.subscribe(subs)  # 可以传递一个元组获取多个订阅源

        while True:
            try:
                self.check_msg()  # 非堵塞检查
                self.ping()  # ping 服务器
                await uasyncio.sleep(1)  # 异步休息
            except Exception as exc:
                print("[ERROR]Sub error:%s" % (exc))
                if eCallback:
                    eCallback()

    async def pub(self, topic: str, msg: str, retries=3, *args, **kw):
        """发布 msg 到主题,重试机制

        Args:
            topic (str): 
            msg (str): 
            retries (int, optional): 重试次数. Defaults to 3.
        """
        content = self.content % self.timestamp

        for _ in range(retries):
            try:
                print(f"send {topic} {content}")
                self.publish(topic, content, *args, **kw)
                return
            except Exception as e:
                print(f"[Error]send err:{e}")
                await uasyncio.sleep(1)
                continue

    def syncPub(self, topic: str, msg: str, retries=3, *args, **kw):
        """同步发布连接"""
        content = self.content % self.timestamp

        for _ in range(retries):
            try:
                print(f"send {topic} {content}")
                self.publish(topic, content, *args, **kw)
                return
            except Exception as e:
                print(f"[Error]send err:{e}")
                continue


if __name__ == "__main__":
    print("wifi disconnect!")
    mqtt = MQTT()
    # uasyncio.run(mqtt.subScribe(__sub_cb))

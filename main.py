# main.py
import utils
import config
from mqttConnect import MQTT
try:
    import uasyncio
except ImportError:
    import asyncio as uasyncio

mqtt = MQTT(
    client_id=config.MQTT_CLIENT_ID,
    server=config.MQTT_SERVER,
    user=config.MQTT_USER,
    password=config.MQTT_PASSWORD,
    port=config.MQTT_PORT
)


async def init():
    # 获取事件循环
    # loop = asyncio.get_event_loop()
    await utils.connectWIFI(
        config.WIFI_SSID,
        config.WIFI_PASSWD
    )
    pass


def callback(topic, msg):
    if "hello" in msg:
        mqtt.pub("/hello/#", msg="我喜欢做爱")


mqtt.cb = callback


async def main():
    tasks = [
        uasyncio.create_task(init()),
        uasyncio.create_task(
            mqtt.subs("/hello/", eCallback=utils.connectWIFI)
        ),
    ]
    await uasyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    uasyncio.run(main())

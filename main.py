# main.py
import utils
import config
from mqttConnect import MQTT
import time
from machine import Pin
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

led = Pin(2, Pin.OUT)  # 板载 led 默认为高电平熄灭


def init():
    """初始化,非异步"""
    while True:
        led.value(0)
        isWifi = utils.connectWIFI(config.WIFI_SSID, config.WIFI_PASSWD)
        if isWifi:
            led.value(1)
            break
        else:
            led.value(1)
            time.sleep(1)

    if utils.sync_ntp():
        print("sync time success!")


def callback(topic, msg):
    print("rev topic:%s msg:%s" % (topic, msg))
    if "hello" in msg:
        mqtt.syncPub("/h/#", msg="我喜欢做爱")


async def main():

    await uasyncio.create_task(
        mqtt.subs(
            "/hello/", cb=callback)
    ),

if __name__ == "__main__":
    init()
    uasyncio.run(main())

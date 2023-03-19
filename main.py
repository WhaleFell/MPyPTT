# main.py
import utils
import config
from mqttConnect import MQTT
import utime
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
    else:
        print("[ERROR]sync time error")

    print("current time:", utils.getTimestamp())


async def eCb():
    while True:
        led.value(0)
        isWifi = utils.connectWIFI(config.WIFI_SSID, config.WIFI_PASSWD)
        if isWifi:
            led.value(1)
            break
        else:
            led.value(1)
            await uasyncio.sleep(3)


mqtt.eCallBack = eCb


def callback(topic, msg):
    print("rev topic:%s msg:%s" % (topic, msg))
    if "hello" in msg:
        mqtt.syncPub("/opopp/", msg="hellppdwww1121")


async def setTime():
    """定时设置时钟"""
    while True:
        await uasyncio.sleep(30*60)
        if utils.sync_ntp():
            print("sync time success!")
        else:
            print("[ERROR]sync time error")
        print("current time:", utils.getTimestamp())


async def main():
    uasyncio.create_task(setTime())

    await uasyncio.create_task(
        mqtt.sub(
            "/hello/", callback=callback)
    ),

if __name__ == "__main__":
    init()
    uasyncio.run(main())

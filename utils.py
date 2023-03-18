# encoding=utf8
# utils.py
import network
import utime
from machine import Pin
import sys
try:
    import uasyncio
except ImportError:
    import asyncio as uasyncio

import dht
import ntptime

### config ####
wifi_ssid = "HomeAP"
wifi_passwd = "992829hws"
###############

wifi = network.WLAN(network.STA_IF)  # 配置wifi模式为station


def handle_error(tries=3):
    """重试函数,异常处理:(带参数的修饰器)
    if func not succes,return False.
    """
    def deco(func):
        def wrapper(*arg, **kw):
            # 写逻辑
            for _ in range(tries):
                try:
                    return func(*arg, **kw)
                except Exception as e:
                    sys.print_exception(e)
            return False
        return wrapper
    return deco


def reversePin(pin: Pin):
    """反转 Pin 高低电平状态"""
    v = pin.value()
    if v:
        pin.value(0)
    else:
        pin.value(1)


def connectWIFI(wifi_ssid: str, wifi_passwd: str, timeout: int = 15) -> bool:
    """连接 WIFI"""
    global wifi

    if not wifi.isconnected():
        print("Connecting to a WIFI network")
        wifi.active(True)
        wifi.connect(wifi_ssid, wifi_passwd)
        i = 0
        print("Connection ing", end="")
        while not wifi.isconnected():
            utime.sleep(1)
            # await uasyncio.sleep(1)
            i += 1
            if i >= timeout:
                print("\nConnection timeout! Please check you SSID or PWD")
                return False
            print(".", end="")

    print("Connection successful!")
    print("network config:", wifi.ifconfig())
    return True
    # ('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')


@handle_error(tries=3)
def sync_ntp() -> bool:
    """通过网络校准时间"""
    ntptime.host = 'ntp1.aliyun.com'
    ntptime.settime()
    return True


def getTimestamp():
    return utime.mktime(utime.localtime())+946656000


if __name__ == "__main__":
    # wifi.disconnect()
    connectWIFI(wifi_ssid, wifi_passwd)

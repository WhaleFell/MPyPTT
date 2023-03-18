# config.py
import ubinascii
import machine


# wifi config
WIFI_SSID = "HomeAP"
WIFI_PASSWD = "992829hws"

# MQTT config
MQTT_SERVER = "broker-cn.emqx.io"
MQTT_PORT = 1883
MQTT_USER = None
MQTT_PASSWORD = None
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_KEEPALIVE = 120  # 设置心跳包时间为 120 秒

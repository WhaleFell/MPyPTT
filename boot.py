# This file is executed on every boot (including wake-boot from deepsleep)
# 该文档在每次启动时执行（包括从 deepsleep 唤醒启动）
# import esp
# esp.osdebug(None)

import uos
import machine

# uos.dupterm(None, 1) # disable REPL on UART(0)

import gc
# import webrepl
# webrepl.start()
gc.collect()

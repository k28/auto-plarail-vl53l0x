#
# ピンのOn-Offを行うコードのサンプル
#
from machine import Pin
import time

p7 = Pin(7, Pin.OUT)
p7.on()

p13 = Pin(13, Pin.OUT)

while True:
    p7.on()
    p13.off()
    time.sleep(1)
    p7.off()
    p13.on()
    time.sleep(1)
    p7.on()
    p13.on()
    time.sleep(1)





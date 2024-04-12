from machine import Pin, I2C
from vl53l0x import VL53L0X

# 距離を測るクラス
class DistanceSensor:

    def __init__(self, tof):
        self.tof = tof
        self._setup()

    def _setup(self):
        self.tof.set_measurement_timing_budget(40000)

        self.tof.set_Vcsel_pulse_period(self.tof.vcsel_period_type[0], 12)
        self.tof.set_Vcsel_pulse_period(self.tof.vcsel_period_type[1], 8)

    # センサで距離を測ります。 単位をmmで返します。
    def scan(self):
        return self.tof.ping() - 50

# 前進, 後退, 停止を制御するクラス
class PlarailController:

    def __init__(self, in1, in2):
        self.in1 = in1
        self.in2 = in2

    def stop(self):
        self.in1.off()
        self.in2.off()
    
    def forward(self):
        self.in1.off()
        self.in2.on()

    def reverse(self):
        self.in1.on()
        self.in2.off()

# 距離によって車両を制御するクラス
class DistanceController:
    # 停止させる距離
    STOP_THRESHOLD = 50

    # 前進させる距離
    FORWARD_THRESHOLD = 100

    def __init__(self, plarailController):
        self.plarailController = plarailController

    def distanceChange(self, distance):
        if distance <= self.STOP_THRESHOLD:
            self.plarailController.stop()
        elif distance >= self.FORWARD_THRESHOLD:
            self.plarailController.forward()

# main

print("setting up i2c")
sda = Pin(14)
scl = Pin(15)
id = 1
i2c = I2C(id=id, sda=sda, scl=scl)
tof = VL53L0X(i2c)
distance_sensor = DistanceSensor(tof)

# コントローラーのピン
in1 = Pin(7, Pin.OUT)
in2 = Pin(13, Pin.OUT)

plarail_controller = PlarailController(in1, in2)
distance_controller = DistanceController(plarail_controller)

while True:
    distance = distance_sensor.scan()
    print(distance, "mm")
    distance_controller.distanceChange(distance)





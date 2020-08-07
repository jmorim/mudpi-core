import time
from .sensor import Sensor

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw

class SoilSensor(Sensor):

    def __init__(self, pin, name = 'SoilSensor', key = None):
        super().__init__(pin, name = name, key = key)
        return
    
    def init_sensor(self):
        i2c_bus = busio.I2C(SCL, SDA)
        ss = Seesaw(i2c_bus, addr = 0x36)
        self.sensor = ss
        return

    def read(self):
        moist = self.sensor.moisture_read()
        temp = self.sensor.get_temp()
        temp_f = round(temp * 9.0 / 5.0 + 32.0, 2)
        print('Moisture:', moist)
        print('Temperature:', temp_f)
#while True:
#    # read moisture level through capacitive touch pad
#    touch = ss.moisture_read()
#
#    # read temperature from the temperature sensor
#    temp = ss.get_temp()
#
#    print("temp: " + str(temp) + "  moisture: " + str(touch))
#    time.sleep(1)

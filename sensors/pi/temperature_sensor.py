import time
import glob
import json
import redis
from .sensor import Sensor
from nanpy import SerialManager
import sys
import RPi.GPIO as GPIO
 

class TemperatureSensor(Sensor):

    def __init__(self, pin, name = 'TemperatureSensor', key = None):
        super().__init__(pin, name = name, key = key)
        return

    def init_sensor(self):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.sensor = device_folder + '/w1_slave'

    def read_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
 
    def read(self):
        lines = self.read_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 2)
#            return temp_c, temp_f
        print('DS18B20 Temp:', temp_f)
 
#while True:
#    print(read_temp())
#    time.sleep(1)
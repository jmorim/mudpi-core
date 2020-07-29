import time
import json
import redis
from .sensor import Sensor
import RPi.GPIO as GPIO
import Adafruit_DHT
import sys
sys.path.append('..')

import variables

#r = redis.Redis(host='127.0.0.1', port=6379)
#PIN MODE : OUT | IN

class HumiditySensor(Sensor):

	def __init__(self, pin, name='HumdityTempSensor', key=None, model='11'):
		super().__init__(pin, name=name, key=key)
		self.type = model
		return

	def init_sensor(self):
		#Initialize the sensor here (i.e. set pin mode, get addresses, etc) this gets called by the worker
		sensor_types = { '11': Adafruit_DHT.DHT11,
						'22': Adafruit_DHT.DHT22,
						'2302': Adafruit_DHT.AM2302 }
		if self.type in sensor_types:
			self.sensor = sensor_types[self.type]
		else:
			print('Sensor Model Error: Defaulting to DHT11')
			self.sensor = Adafruit_DHT.DHT11
		return

	def read(self):
		#Read the sensor(s), parse the data and store it in redis if redis is configured

		humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
		
		if humidity is not None or temperature is not None:
			variables.r.set(self.key + '_temperature', round(temperature * 1.8 + 32, 2))
			variables.r.set(self.key + '_humidity', humidity)
			readings = {'temperature': round(temperature * 1.8 + 32, 2), 'humidity': humidity}
			variables.r.set(self.key, json.dumps(readings))
			print('Pi Temp:', readings)
			return readings
		else:
			print('Failed to get reading. Try again!')


	def readRaw(self):
		#Read the sensor(s) but return the raw data, useful for debugging
		return self.read()

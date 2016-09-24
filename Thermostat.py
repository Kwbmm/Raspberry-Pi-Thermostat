#!/usr/bin/python

from gpiozero import InputDevice, OutputDevice
from gpiozero.pins.rpigpio import RPiGPIOPin as RGP
import time
import math


class ThermostatSensor:
	"""Class that manages temperature readings"""

	# uF - Tweek this value around 0.33 to improve accuracy
	C = 0.38
	R1 = 1000  # Ohms
	# The thermistor constant - change this for a different thermistor
	B = 3800.0
	# The resistance of the thermistor at 25C -change for different thermistor
	R0 = 1000.0
	n = 100  # Number of readings
	chargeDevice = None
	dischargeDevice = None

	chargePin = -1
	dischargePin = -1

	def __init__(self, chargePin, dischargePin):
		self.chargePin = chargePin
		self.dischargePin = dischargePin

	def getTemp(self):
		return self.__read_temp_c()

	def __read_temp_c(self):
		R = self.__read_resistance()
		t0 = 273.15  # 0 degrees C in K
		t25 = t0 + 25.0
		invT = 1 / t25 + 1 / self.B * math.log(R / self.R0)
		T = (1 / invT - t0)
		return T

	def __read_resistance(self):
		total = 0
		for i in range(0, self.n):
			total += self.__analog_read()
		print "__read_resistance: total from analog read=" + str(total)
		t = total / float(self.n)
		print "__read_resistance: total divided by n=" + str(t)
		T = t * 0.632 * 3.3
		print "__read_resistance: big T=" + str(T)
		r = (T / self.C) - self.R1
		print "__read_resistance: resistance=" + str(r)
		return r

	def __analog_read(self):
		"""
		Take an analog reading as the time taken to charge after first discharging
		the capacitor
		"""
		self.__discharge()
		t = self.__charge_time()
		self.__discharge()
		print "Time taken to charge=" + str(t)
		return t

	def __discharge(self):
		self.__closeDevices()
		self.chargeDevice = InputDevice(self.chargePin)
		self.dischargeDevice = OutputDevice(self.dischargePin)
		time.sleep(0.01)

	def __charge_time(self):
		"""
		Return the time taken for the voltage on the capacitor to count as a digital
		input HIGH than means around 1.65V
		"""
		self.__closeDevices()
		self.dischargeDevice = InputDevice(self.dischargePin)
		self.chargeDevice = OutputDevice(self.chargePin, True, True)
		t1 = time.time()
		# While input is LOW
		while not self.dischargeDevice.is_active:
			pass
		t2 = time.time()
		return (t2 - t1) * 1000000  # uS

	def __closeDevices(self):
		if self.chargeDevice is not None and self.dischargeDevice is not None:
			self.chargeDevice.close()
			self.dischargeDevice.close()


t = ThermostatSensor(18, 23)
while True:
	print t.getTemp()

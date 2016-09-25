#!/usr/bin/python

import RPi.GPIO as GPIO
from gpiozero import Button
import time
import math


class ThermostatSensor:
	"""Class that manages temperature readings"""

	# uF - Tweek this value around 0.33 to improve accuracy
	C = 0.33
	R1 = 1000  # Ohms
	# The thermistor constant - change this for a different thermistor
	B = 3800.0
	# The resistance of the thermistor at 25C -change for different thermistor
	R0 = 1000.0
	n = -1  # Number of readings

	chargePin = -1
	dischargePin = -1

	def __init__(self, chargePin, dischargePin, readingNum=100):
		GPIO.setmode(GPIO.BCM)
		self.chargePin = chargePin
		self.dischargePin = dischargePin
		self.n = readingNum

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		GPIO.cleanup()

	def getTemp(self):
		return self._read_temp_c()

	def _read_temp_c(self):
		R = self._read_resistance()
		t0 = 273.15  # 0 degrees C in K
		t25 = t0 + 25.0
		invT = 1 / t25 + 1 / self.B * math.log(R / self.R0)
		T = (1 / invT - t0)
		return T

	def _read_resistance(self):
		total = 0
		for i in range(0, self.n):
			total += self._analog_read()
		total /= float(self.n)
		T = total * 0.632 * 3.3
		r = (T / self.C) - self.R1
		return r

	def _analog_read(self):
		"""
		Take an analog reading as the time taken to charge after first discharging
		the capacitor
		"""
		self._discharge()
		t = self._charge_time()
		self._discharge()
		return t

	def _discharge(self):
		GPIO.setup(self.chargePin, GPIO.IN)
		GPIO.setup(self.dischargePin, GPIO.OUT)
		GPIO.output(self.dischargePin, False)
		time.sleep(0.01)

	def _charge_time(self):
		"""
		Return the time taken for the voltage on the capacitor to count as a digital
		input HIGH than means around 1.65V
		"""
		GPIO.setup(self.dischargePin, GPIO.IN)
		GPIO.setup(self.chargePin, GPIO.OUT)
		GPIO.output(self.chargePin, True)
		t1 = time.time()
		# While input is LOW
		while not GPIO.input(self.dischargePin):
			pass
		t2 = time.time()
		return (t2 - t1) * 1000000  # uS


counter = 20


def btnUpPress():
	counter += 1
	print counter


def btnDownPress():
	counter -= 1
	print counter

btnUp = Button(8)
btnUp.when_pressed = btnUpPress
btnDown = Button(7)
btnDown.when_pressed = btnDownPress
with ThermostatSensor(18, 23) as t:
	while True:
		print t.getTemp()

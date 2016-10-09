#!/usr/bin/python

from Thermostat import ThermostatSensor
from Display import DisplayDevice
from gpiozero import Button
from pydispatch import dispatcher
from decimal import *
from threading import Timer
import datetime
import time
import sqlite3
from signal import pause


class Controller:
	"""Manages all the other components and signalling"""

	BTN_UP_TO_DISPLAY_SIG = "HELLO-DISPLAY-IM-BTN-UP"
	BTN_DOWN_TO_DISPLAY_SIG = "HELLO-DISPLAY-IM-BTN-DOWN"
	startTargetTemp = 20

	def __init__(self):
		self.thermostat = ThermostatSensor(18, 23)
		dispatcher.connect(self.signalHandler, signal=self.thermostat.THERMOSTAT_TO_CONTROLLER_SIG, sender=dispatcher.Any)
		print "Thermostat init"

		self.startTargetTemp = self._fetchTargetTemp(self.startTargetTemp)
		self.display = DisplayDevice(0x3F, self.thermostat, self.startTargetTemp, self)
		print "Display init"

		self.btnUp = Button(8)
		self.btnDown = Button(7)
		self.btnUp.when_pressed = self._sendIncrease
		self.btnDown.when_pressed = self._sendDecrease
		print "Buttons init"

		self.isActive = 0
		print "Launching getTemp().."
		self.thermostat.readTemp.start()
		print "Launched!"

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.thermostat.close()

	def signalHandler(self, sender, param):
		"""
		Here we should act differently according to which is the sender: param may
		contain different data based on which component sent the signal
		"""
		if sender == self.thermostat:
			# Save into temperature_log the temp and a time record
			conn = sqlite3.connect("thermostat.db")
			conn.execute("BEGIN EXCLUSIVE TRANSACTION")
			cur = conn.cursor()
			sql = """
					INSERT INTO temperature_log(temp, timeRecord, isActive)
					VALUES(?, ?, ?)
				"""
			cur.execute(sql, (param['temp'], time.time(), self.isActive))
			if cur.rowcount != 1:
				conn.rollback()
			else:
				conn.commit()
		else:
			print "Wrong sender"

	def _fetchTargetTemp(self, target):
		now = time.time()
		todayWeekDay = datetime.datetime.today().weekday() + 1
		todayHour = time.strftime("%H")
		sql = """	SELECT targetTemp FROM program
					WHERE weekDay = ?
					AND hour = ?
			"""
		conn = sqlite3.connect("thermostat.db")
		cur = conn.cursor()
		cur.execute(sql, (todayWeekDay, todayHour))
		result = cur.fetchone()
		if result is not None:
			return result[0]
		else:
			return targetTemp

	def _sendIncrease(self):
		dispatcher.send(signal=self.BTN_UP_TO_DISPLAY_SIG, sender=self, param=1)

	def _sendDecrease(self):
		dispatcher.send(signal=self.BTN_DOWN_TO_DISPLAY_SIG, sender=self, param=-1)

if __name__ == '__main__':
	with Controller() as manager:
		pause()

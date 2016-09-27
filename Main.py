#!/usr/bin/python

from Thermostat import ThermostatSensor
from Display import DisplayDevice
from gpiozero import Button
from pydispatch import dispatcher
from decimal import *
from threading import Timer
import time
import sqlite3
import signal


class Controller:
	"""Manages all the other components and signalling"""
	def __init__(self):
		dispatcher.connect(self.signalHandler, signal=dispatcher.Any, sender=dispatcher.Any)
		self.thermostat = ThermostatSensor(18, 23)
		print "Thermostat init"
		# self.display = DisplayDevice(20)
		# self.btnUp = Button(8)
		# self.btnDown = Button(7)
		self.isActive = 0
		print "Launching getTemp().."
		self.thermostat.readTemp.start()
		print "Launched!"

	def signalHandler(self, sender, param):
		"""
		Here we should act differently according to which is the sender: param may
		contain different data based on which component sent the signal
		"""
		if sender == self.thermostat:
			print "Saving fetched temp"
			# Save into temperature_log the temp and a time record
			conn = sqlite3.connect("thermostat.db")
			conn.execute("BEGIN EXCLUSIVE TRANSACTION")
			cur = conn.cursor()
			sql = """
					INSERT INTO temperature_log(temp, timeRecord, isActive)
					VALUES(?, ?, ?)
				"""
			print "Inserting temp: ", param['temp']
			cur.execute(sql, (float(param['temp']), time.time(), self.isActive))
			if cur.rowcount != 1:
				conn.rollback()
				print "Insert failed"
			else:
				conn.commit()
				print "Success"
		else:
			print "Wrong sender"

if __name__ == '__main__':
	manager = Controller()

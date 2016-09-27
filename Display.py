#!/usr/bin/python
import sqlite3
import datetime
import time
from pydispatch import dispatcher


class DisplayDevice:
#	lastManualChange = -1

	"""Manages data on the display"""
	def __init__(self, thermostatSensor):
		self.thermostatSensor = thermostatSensor
		dispatcher.connect(self.updateEnvTempScreen, signal=self.thermostatSensor.THERMOSTAT_TO_DISPLAY_SIG, sender=self.thermostatSensor)

	def updateEnvTempScreen(self, sender, param):
		print "Environment Temperature: ", param

#	def _fetchTargetTemp(self, target):
#		now = time.time()
#		# Take the temp from the DB only if the last update was
#		# more than 2 minutes ago
#		if now - self.lastManualChange >= 120 and self.lastManualChange != -1:
#			print "updating from db"
#			todayWeekDay = datetime.datetime.today().weekday() + 1
#			todayHour = time.strftime("%H")
#			sql = """	SELECT targetTemp FROM program
#						WHERE weekDay = ?
#						AND hour = ?
#				"""
#			conn = sqlite3.connect("thermostat.db")
#			cur = conn.cursor()
#			cur.execute(sql, (todayWeekDay, todayHour))
#			result = cur.fetchone()
#			if result is not None:
#				self.targetTemp = result[0]
#			else:
#				self.targetTemp = targetTemp
#		self.updateScreen(self.currentTemp)
#		Timer(5, self._fetchTargetTemp, [target]).start()
#
#	def increaseTargetTemp(self):
#		print "Increase temp"
#		self.targetTemp += 1
#		self.lastManualChange = time.time()
#		self.updateScreen(self.currentTemp)
#
#	def decreaseTargetTemp(self):
#		print "Decrease temp"
#		self.targetTemp -= 1
#		self.lastManualChange = time.time()
#		self.updateScreen(self.currentTemp)
#
#	def updateScreen(self, current):
#		"""Here we should manage the refresh of the data displayed on the screen"""
#		self.currentTemp = current
#		print "Target is: " + str(self.targetTemp)
#		print "Current is: " + str(self.currentTemp)

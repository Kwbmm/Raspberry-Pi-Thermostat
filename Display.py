#!/usr/bin/python
import sqlite3
import datetime
import time
from threading import Timer


class DisplayDevice:
	targetTemp = -1
	currentTemp = -1
	lastManualChange = -1

	"""Manages data on the display"""
	def __init__(self, targetTemp):
		"""Init data for the display"""
		self._fetchTargetTemp()

	def _fetchTargetTemp(self):
		now = time.time()
		# Take the temp from the DB only if the last update was
		# more than 2 minutes ago
		if now - self.lastManualChange >= 120:
			print "updating from db"
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
				self.targetTemp = result[0]
			else:
				self.targetTemp = targetTemp
		self.updateScreen(self.currentTemp)
		Timer(5, self._fetchTargetTemp).start()

	def increaseTargetTemp(self):
		self.targetTemp += 1
		self.lastManualChange = time.time()
		self.updateScreen(self.currentTemp)

	def decreaseTargetTemp(self):
		self.targetTemp -= 1
		self.lastManualChange = time.time()
		self.updateScreen(self.currentTemp)

	def updateScreen(self, current):
		"""Here we should manage the refresh of the data displayed on the screen"""
		self.currentTemp = current
		print "Target is: " + str(self.targetTemp)
		print "Current is: " + str(self.currentTemp)

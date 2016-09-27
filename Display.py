#!/usr/bin/python
import sqlite3
import datetime
import time
from pydispatch import dispatcher


class DisplayDevice:
#	lastManualChange = -1

	"""Manages data on the display"""
	def __init__(self, thermostatSensor, targetTemp, controller):
		self.thermostatSensor = thermostatSensor
		self.controller = controller
		self.targetTemp = targetTemp
		dispatcher.connect(self.updateEnvTempScreen, signal=self.thermostatSensor.THERMOSTAT_TO_DISPLAY_SIG, sender=self.thermostatSensor)
		dispatcher.connect(self.updateTargetTempScreen, signal=self.controller.BTN_UP_TO_DISPLAY_SIG, sender=self.controller)
		dispatcher.connect(self.updateTargetTempScreen, signal=self.controller.BTN_DOWN_TO_DISPLAY_SIG, sender=self.controller)

	def updateEnvTempScreen(self, sender, param):
		print "Environment Temperature: ", param

	def updateTargetTempScreen(self, sender, param):
		self.targetTemp += param
		print "Target Temperature: ", self.targetTemp

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

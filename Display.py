#!/usr/bin/python


class DisplayDevice:
	targetTemp = -1
	currentTemp = -1
	"""Manages data on the display"""
	def __init__(self, targetTemp):
		"""Init data for the display"""
		self.targetTemp = targetTemp

	def increaseTargetTemp(self):
		self.targetTemp += 1
		self.updateScreen(self.currentTemp)

	def decreaseTargetTemp(self):
		self.targetTemp -= 1
		self.updateScreen(self.currentTemp)

	def updateScreen(self, current):
		"""Here we should manage the refresh of the data displayed on the screen"""
		self.currentTemp = current
		print "Target is: " + str(self.targetTemp)
		print "Current is: " + str(self.currentTemp)

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
		self.updateScreen(self.targetTemp, self.currentTemp)

	def decreaseTargetTemp(self):
		self.targetTemp -= 1
		self.updateScreen(self.targetTemp, self.currentTemp)

	def updateScreen(self, target, current):
		"""Here we should manage the refresh of the data displayed on the screen"""
		if target is None:
			print "Target is: " + str(self.targetTemp)
		else:
			print "Target is: " + str(target)
		print "Current is: " + str(current)

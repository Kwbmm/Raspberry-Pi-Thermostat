#!/usr/bin/python
import sqlite3
import datetime
import time
import smbus
from pydispatch import dispatcher


class DisplayDevice:

	# Define some device constants
	LCD_CHR = 1  # Mode - Sending data
	LCD_CMD = 0  # Mode - Sending command

	LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
	LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
	LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
	LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

	LCD_BACKLIGHT = 0x08  # On
	ENABLE = 0b00000100  # Enable bit

	# Timing constants
	E_PULSE = 0.0005
	E_DELAY = 0.0005

	"""Manages data on the display"""
	def __init__(self, displayAddress, thermostatSensor, targetTemp, controller, displayWidth=20):
		self.bus = smbus.SMBus(1)
		self.thermostatSensor = thermostatSensor
		self.controller = controller
		self.targetTemp = targetTemp
		self.i2cAddr = displayAddress
		self.displayWidth = displayWidth
		self._lcdByte(0x33, self.LCD_CMD)  # 110011 Initialise
		self._lcdByte(0x32, self.LCD_CMD)  # 110010 Initialise
		self._lcdByte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
		self._lcdByte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
		self._lcdByte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
		self._lcdByte(0x01, self.LCD_CMD)  # 000001 Clear display


		dispatcher.connect(self.updateEnvTempScreen, signal=self.thermostatSensor.THERMOSTAT_TO_DISPLAY_SIG, sender=self.thermostatSensor)
		dispatcher.connect(self.updateTargetTempScreen, signal=self.controller.BTN_UP_TO_DISPLAY_SIG, sender=self.controller)
		dispatcher.connect(self.updateTargetTempScreen, signal=self.controller.BTN_DOWN_TO_DISPLAY_SIG, sender=self.controller)

	def _lcdByte(self, bits, mode):
		# Send byte to data pins
		# bits = the data
		# mode = 1 for data
		#        0 for command
		bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
		bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT
		# High bits
		self.bus.write_byte(self.i2cAddr, bits_high)
		self._lcdToggleEnable(bits_high)
		# Low bits
		self.bus.write_byte(self.i2cAddr, bits_low)
		self._lcdToggleEnable(bits_low)

	def _lcdToggleEnable(self, bits):
		# Toggle enable
		self.bus.write_byte(self.i2cAddr, (bits | self.ENABLE))
		self.bus.write_byte(self.i2cAddr, (bits & ~self.ENABLE))

	def _lcdString(self, message, line):
		message = message.ljust(self.displayWidth, " ")
		self._lcdByte(line, self.LCD_CMD)
		for i in range(self.displayWidth):
			self._lcdByte(ord(message[i]), self.LCD_CHR)

	def updateEnvTempScreen(self, sender, param):
		self._lcdString("Env Temp: " + str(param), self.LCD_LINE_1)

	def updateTargetTempScreen(self, sender, param):
		self.targetTemp += param
		self._lcdString("Target Temp: " + str(param), self.LCD_LINE_2)

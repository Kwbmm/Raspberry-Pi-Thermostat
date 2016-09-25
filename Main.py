#!/usr/bin/python

from Thermostat import ThermostatSensor
from Display import DisplayDevice
from gpiozero import Button


display = DisplayDevice(20)
btnUp = Button(8)
btnUp.when_pressed = display.increaseTargetTemp
btnDown = Button(7)
btnDown.when_pressed = display.decreaseTargetTemp
with ThermostatSensor(18, 23) as t:
	while True:
		display.updateScreen(None, t.getTemp())

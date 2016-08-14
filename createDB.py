#!/usr/bin/python 
import sqlite3

connection = sqlite3.connect("thermostat.db")
connection.executescript("""
	CREATE TABLE temperature_log(
		TID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
		temp INTEGER NOT NULL, 
		timeRecord INTEGER NOT NULL, 
		isActive INTEGER DEFAULT 0
	);
	CREATE TABLE program(
		PID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
		weekDay INTEGER NOT NULL,
		hour INTEGER NOT NULL,
		targetTemp INTEGER NOT NULL DEFAULT 24
	);
	""")
import web
import sqlite3
import time
from web.contrib.template import render_jinja

render = render_jinja('templates', encoding='utf-8')


class Program():
	def GET(self, day):
		data = self.__getWeekDays(day)
		return render.program(data=data, day=day, domain=web.ctx.homedomain)

	def __getWeekDays(self, day):
		if day == "monday":
			sql = "SELECT hour, targetTemp FROM program WHERE weekDay = 1 ORDER BY hour"
		elif day == "tuesday":
			sql = "SELECT hour, targetTemp FROM program WHERE weekDay = 2 ORDER BY hour"
		elif day == "wednesday":
			sql = "SELECT hour, targetTemp FROM program WHERE weekDay = 3 ORDER BY hour"
		elif day == "thursday":
			sql = "SELECT hour, targetTemp FROM program WHERE weekDay = 4 ORDER BY hour"
		elif day == "friday":
			sql = "SELECT hour, targetTemp FROM program WHERE weekDay = 5 ORDER BY hour"
		elif day == "saturday":
			sql = "SELECT hour, targetTemp FROM program WHERE weekDay = 6 ORDER BY hour"
		elif day == "sunday":
			sql = "SELECT hour, targetTemp FROM program WHERE weekDay = 7 ORDER BY hour"
		conn = sqlite3.connect("thermostat.db")
		cur = conn.cursor()
		cur.execute(sql)
		result = cur.fetchall()
		returnData = []
		for row in result:
			returnData.append(row[1])
		return returnData

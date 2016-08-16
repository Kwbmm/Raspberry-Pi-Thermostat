import web
import sqlite3
import time
from web.contrib.template import render_jinja

render = render_jinja('templates', encoding='utf-8')


class Program():
	def GET(self, day):
		data = self.__getWeekDays()
		data["day"] = day
		return render.program(data=data, domain=web.ctx.homedomain)

	def __getWeekDays(self):
		sql = "SELECT weekDay, hour, targetTemp FROM program ORDER BY weekDay, hour"
		conn = sqlite3.connect("thermostat.db")
		cur = conn.cursor()
		cur.execute(sql)
		result = cur.fetchall()
		returnData = {}
		for row in result:
			if row[0] == 1:
				returnData["Monday"] = {'hour': row[1], 'temp': row[2]}
			elif row[0] == 2:
				returnData["Tuesday"] = {'hour': row[1], 'temp': row[2]}
			elif row[0] == 3:
				returnData["Wednesday"] = {'hour': row[1], 'temp': row[2]}
			elif row[0] == 4:
				returnData["Thursday"] = {'hour': row[1], 'temp': row[2]}
			elif row[0] == 5:
				returnData["Friday"] = {'hour': row[1], 'temp': row[2]}
			elif row[0] == 6:
				returnData["Saturday"] = {'hour': row[1], 'temp': row[2]}
			elif row[0] == 7:
				returnData["Sunday"] = {'hour': row[1], 'temp': row[2]}
			else:
				returnData["error"] = True
		return returnData

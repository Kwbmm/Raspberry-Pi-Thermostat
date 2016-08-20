import web
import sqlite3
import time
from web.contrib.template import render_jinja

render = render_jinja('templates', encoding='utf-8')


class Program():
	def GET(self, day):
		data = self.__getWeekDays(day)
		if len(data) == 0:
			return render.program(data=None, day=day, domain=web.ctx.homedomain)
		return render.program(data=data, day=day, domain=web.ctx.homedomain)

	def POST(self, day):
		data = web.input()
		num = self.__weekDayString2Num(day)
		sql = "SELECT targetTemp FROM program WHERE weekDay = ? AND hour = ?"
		conn = sqlite3.connect("thermostat.db")
		output = []
		conn.execute("BEGIN EXCLUSIVE TRANSACTION")
		for rawHour, temp in data.items():
			hour = rawHour.split("-")
			hour = hour[1]
			cur = conn.cursor()
			cur.execute(sql, (num, hour))
			result = cur.fetchall()
			if len(result) == 0:  # There is no data in the DB
				insertSql = "INSERT INTO program (weekDay,hour,targetTEmp) VALUES(?,?,?)"
				cur.execute(insertSql, (num, hour, temp))
				if cur.rowcount != 1:
					conn.rollback()
					return render.program(data=None, day=day, domain=web.ctx.homedomain)
			else:
				updateSql = "UPDATE program SET targetTemp = ? WHERE weekDay = ? AND hour = ?"
				cur.execute(updateSql, (temp, num, hour))
				if cur.rowcount != 1:
					conn.rollback()
					return render.program(data=None, day=day, domain=web.ctx.homedomain)
		conn.commit()
		return render.program(data=self.__getWeekDays(day), day=day, domain=web.ctx.homedomain)

	def __getWeekDays(self, day):
		num = self.__weekDayString2Num(day)
		sql = "SELECT hour, targetTemp FROM program WHERE weekDay = ? ORDER BY hour"
		conn = sqlite3.connect("thermostat.db")
		cur = conn.cursor()
		cur.execute(sql, (num,))
		result = cur.fetchall()
		returnData = []
		for row in result:
			returnData.append(row[1])
		return returnData

	def __weekDayNum2String(self, day):
		if day == 1:
			return 'monday'
		elif day == 2:
			return 'tuesday'
		elif day == 3:
			return 'wednesday'
		elif day == 4:
			return 'thursday'
		elif day == 5:
			return 'friday'
		elif day == 6:
			return 'saturday'
		elif day == 7:
			return 'sunday'
		else:
			return None

	def __weekDayString2Num(self, day):
		if day == 'monday':
			return 1
		elif day == 'tuesday':
			return 2
		elif day == 'wednesday':
			return 3
		elif day == 'thursday':
			return 4
		elif day == 'friday':
			return 5
		elif day == 'saturday':
			return 6
		elif day == 'sunday':
			return 7
		else:
			return None

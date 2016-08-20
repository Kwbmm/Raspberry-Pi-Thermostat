import web
import sqlite3
import time
from web.contrib.template import render_jinja

render = render_jinja('templates', encoding='utf-8')


class Home:
	def GET(self):
		data = {}
		now = int(time.time())
		sql = """
				SELECT temp, isActive, timeRecord
				FROM temperature_log
				WHERE timeRecord <= ?
				ORDER BY timeRecord DESC
				LIMIT 1
			"""
		conn = sqlite3.connect("thermostat.db")
		cur = conn.cursor()
		cur.execute(sql, (now,))
		result = cur.fetchone()
		if result is not None:
			timeDiff = now - result[2]
			data["isActive"] = result[1]
			data["temp"] = result[0]
			if timeDiff < 30:
				data['timeRecord'] = "some seconds ago"
			elif timeDiff >= 30 and timeDiff < 60:
				data['timeRecord'] = str(timeDiff) + " seconds ago"
			elif timeDiff >= 60 and timeDiff < 3600:
				mins, secs = divmod(timeDiff, 60)
				data['timeRecord'] = str(mins) + ' minutes ago'
			elif timeDiff >= 3600 and timeDiff < 7200:
				data['timeRecord'] = "an hour and something ago"
			elif timeDiff >= 7200 and timeDiff < 86400:
				mins, secs = divmod(timeDiff, 60)
				hours, mins = divmod(mins, 60)
				data['timeRecord'] = str(hours) + " hours ago"
			else:
				data['timeRecord'] = "a long time ago..."				
		else:
			data["isActive"] = None
			data["temp"] = None
			data["timeRecord"] = None

		return render.home(data=data, domain=web.ctx.homedomain)

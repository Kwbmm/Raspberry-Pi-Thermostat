import web
import sqlite3
import time
from web.contrib.template import render_jinja

render = render_jinja('templates', encoding='utf-8')


class Program():
	def GET(self):
		return render.program()

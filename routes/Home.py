import web
from web.contrib.template import render_jinja

render = render_jinja('templates', encoding='utf-8')


class Home:
	def GET(self):
		return render.home(appName="Thermostat")

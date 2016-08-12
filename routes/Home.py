import web
from Menu import *

render = web.template.render('templates/', base="base")


class Home:
	def GET(self):
		return render.home(getURLs())

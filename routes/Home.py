import web
import Menu

render = web.template.render('templates/', base="base")


class Home:
	def GET(self):
		return render.home(getURLs())

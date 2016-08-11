import web

render = web.template.render('../templates/')


class Home:
	def GET(self):
		return render.home("Marco")

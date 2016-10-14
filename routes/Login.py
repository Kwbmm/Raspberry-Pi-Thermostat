import web
from web.contrib.template import render_jinja

render = render_jinja('templates', encoding='utf-8')


class Login:
    """Manages Login"""
    def GET(self):
        data = web.input(return_to="/")
        return render.login(domain=web.ctx.homedomain)

    def POST(self):
        data = web.input()
        return render.login(domain=web.ctx.homedomain, data=data.items())

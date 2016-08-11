#!/usr/bin/env python

import web
from routes.Home import Home

render = web.template.render('templates/')

if __name__ == "__main__":
	app = web.application(('/*', 'Home'), globals())
	app.run()

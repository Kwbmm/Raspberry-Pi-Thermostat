#!/usr/bin/env python

import web
from routes.Home import Home
from routes.Program import Program

urls = (
	'/', 'Home',
	'/program/(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', 'Program'
)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

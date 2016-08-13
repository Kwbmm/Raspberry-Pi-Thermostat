#!/usr/bin/env python

import web
from routes.Home import Home

urls = (
	'/', 'Home'
)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

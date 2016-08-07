#!/usr/bin/env python

import web
import routes

if __name__ == "__main__":
	app = web.application(('/*', 'index'), globals())
	app.run()

#!/usr/bin/env python

import web
from routes.Home import Home


if __name__ == "__main__":
	app = web.application(('/*', 'Home'), globals())
	app.run()

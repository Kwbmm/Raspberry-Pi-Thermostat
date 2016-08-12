#!/usr/bin/env python

import web
from routes.Home import Home
from routes import Menu


if __name__ == "__main__":
	app = web.application(getURLs(), globals())
	app.run()

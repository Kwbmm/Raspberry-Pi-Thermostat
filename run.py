#!/usr/bin/env python

import web
from routes.Home import Home
from routes.Menu import *


if __name__ == "__main__":
	app = web.application(getURLs(), globals())
	app.run()

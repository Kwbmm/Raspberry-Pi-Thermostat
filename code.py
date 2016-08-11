#!/usr/bin/env python

import web
from routes.index import Index

if __name__ == "__main__":
	app = web.application(('/*', 'Index'), globals())
	app.run()

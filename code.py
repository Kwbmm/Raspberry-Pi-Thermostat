#!/usr/bin/python3

import web

# Say hello.


class Index:
	def GET(self):
		return 'hello web.py'

if __name__ == "__main__":
	app = web.application(('/*', 'Index'), globals())
	app.run()

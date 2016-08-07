#!/usr/bin/python3

from routes import Index

if __name__ == "__main__":
	app = web.application(('/*', 'Index'), globals())
	app.run()

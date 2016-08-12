import web

render = web.template.render('templates/')


def getURLs():
	urls = (
		'/', 'Home'
	)
	return urls

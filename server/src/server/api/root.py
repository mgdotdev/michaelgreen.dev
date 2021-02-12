import cherrypy

@cherrypy.expose
class Example(object):
    def GET(self):
        return "This is New!"

@cherrypy.expose
class ApiRoot(object):
    def GET(self):
        return "Hello from API!"
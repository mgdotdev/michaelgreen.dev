import cherrypy

from .utils import templates

class Root:
    @cherrypy.expose
    def index(self):
        with open(templates("index.html")) as f:
            return f.read()


class Portfolio:
    @cherrypy.expose
    def index(self):
        with open(templates.portfolio("index.html")) as f:
            return f.read()

    @cherrypy.expose
    def CompGen(self):
        with open(templates.portfolio("CompGen.html")) as f:
            return f.read()

    @cherrypy.expose
    def libRL(self):
        with open(templates.portfolio("libRL.html")) as f:
            return f.read() 
            
    @cherrypy.expose
    def pyGC(self):
        with open(templates.portfolio("pyGC.html")) as f:
            return f.read()                

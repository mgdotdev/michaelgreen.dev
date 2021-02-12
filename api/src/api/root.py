import cherrypy


class ApiRoot:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"response": "Welcome to the API!"}

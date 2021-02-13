import cherrypy
import requests


class Resume:
    @cherrypy.expose
    @cherrypy.tools.json_out(content_type="application/json")
    def index(self):
        return requests.get(
            "https://gist.githubusercontent.com/1mikegrn/"
            "5b35c4cf10c43e2d8a001e1509c0788c/raw/"
            "290469a6996ccc46b5c56a34e8a583d942c76d94/resume.json"
        ).json()

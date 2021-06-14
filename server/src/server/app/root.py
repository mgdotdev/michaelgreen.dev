import cherrypy
import requests

from jinja2 import Template

from .utils import templates
from ..settings import SETTINGS

class Root:
    @cherrypy.expose
    def index(self):
        citations = requests.get(
            "https://api.michaelgreen.dev/v1/webscraping/googlescholarcitations"
        ).json()
        with open(templates()) as f:
            template = Template(f.read())
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"],
            citations=citations['citations'], 
            h_index=citations['h-index'], 
            i_index=citations['i-index']
        )
        return render


class Portfolio:
    @cherrypy.expose
    def index(self):
        with open(templates.portfolio()) as f:
            template = Template(f.read())
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"]
        )
        return render

    @cherrypy.expose
    def CompGen(self):
        with open(templates.portfolio("CompGen.html")) as f:
            template = Template(f.read())
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"]
        )
        return render

    @cherrypy.expose
    def libRL(self):
        with open(templates.portfolio("libRL.html")) as f:
            template = Template(f.read())
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"]
        )
        return render
            
    @cherrypy.expose
    def pyGC(self):
        with open(templates.portfolio("pyGC.html")) as f:
            template = Template(f.read())  
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"]
        )
        return render

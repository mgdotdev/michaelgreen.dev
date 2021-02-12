import cherrypy

from .personal_info import DEFAULT_CITATION_RESULTS, _get_citation_metrics

class WebScraping:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"whoami": "index for api endpoint, webscrapers"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def googlescholarcitations(self):
        try:
            return _get_citation_metrics()
        except:
            return DEFAULT_CITATION_RESULTS
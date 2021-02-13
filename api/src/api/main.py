import cherrypy

from .root import ApiRoot
from .resume.resume import Resume
from .web_scraping.base import WebScraping

config = {}
# config = {
#     '/': {
#         'request.dispatch': cherrypy.dispatch.MethodDispatcher()
#     },
#     '/webscraping': {
#         'request.dispatch': cherrypy.dispatch.RoutesDispatcher()
#     }
# }

def main():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0'
        })

    api = ApiRoot()
    api.webscraping = WebScraping()
    api.resume = Resume()

    cherrypy.tree.mount(api, '/v1', config)
    
    cherrypy.engine.start()
    cherrypy.engine.block()    
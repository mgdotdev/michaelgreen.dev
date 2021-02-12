import cherrypy

from .app.root import Root, Portfolio
from .api.root import ApiRoot, Example

method_dispatch = {
    '/': {
    'request.dispatch': cherrypy.dispatch.MethodDispatcher()
    }
}

app_config = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': "/code/client"
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './static'
    }
}

def main():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0'
        })

    app = Root()
    app.portfolio = Portfolio()

    api = ApiRoot()
    api.example = Example()

    cherrypy.tree.mount(app, '/', app_config)
    cherrypy.tree.mount(api, '/api/v1', method_dispatch)

    cherrypy.engine.start()
    cherrypy.engine.block()

import cherrypy

from .app.root import Root, Portfolio

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

    cherrypy.tree.mount(app, '/', app_config)

    cherrypy.engine.start()
    cherrypy.engine.block()

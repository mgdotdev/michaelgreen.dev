import cherrypy

from .app.root import Node, _append_nodes
from .settings import SETTINGS


def main():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0'
        })

    app = Node()
    _append_nodes(app)

    cherrypy.tree.mount(app, '/', SETTINGS["blog"]["app_config"])

    cherrypy.engine.start()
    cherrypy.engine.block()

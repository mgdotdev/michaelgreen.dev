import cherrypy

from .app.root import Root
from .settings import SETTINGS


def main():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0'
        })

    app = Root()

    cherrypy.tree.mount(app, '/', SETTINGS["blog"]["app_config"])

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    main()
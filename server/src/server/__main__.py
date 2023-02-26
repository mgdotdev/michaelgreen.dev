import os

import cherrypy

from .app.root import Root, Portfolio
from .settings import SETTINGS

def main():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get("PORT", '8080')),
        })

    app = Root()
    app.portfolio = Portfolio()

    cherrypy.tree.mount(app, '/', SETTINGS["server"]["app_config"])

    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == "__main__":
    main()

import os

STATIC_ASSETS = os.environ.get("STATIC_ASSETS")

app_config = {
    '/': {
        'tools.sessions.on': True
    }
}

if STATIC_ASSETS:
    app_config["/"].update({'tools.staticdir.root': "/code/server/client"})
    app_config.update({
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    })

SETTINGS = {
    "client": {
        "static_assets": STATIC_ASSETS or "https://storage.googleapis.com/michaelgreendev/server/client/static"
    },
    "server": {
        "app_config": app_config
    }
}
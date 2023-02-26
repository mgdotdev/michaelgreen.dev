import os

STATIC_ASSETS = os.environ.get(
    "STATIC_ASSETS", 
    "https://storage.googleapis.com/michaelgreendev/server/client/static"
)

app_config = {
    '/': {
        'tools.sessions.on': True
    }
}

if not STATIC_ASSETS.startswith("https://"):
    app_config["/"].update({'tools.staticdir.root': "/code/server/client"})
    app_config.update({
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    })

SETTINGS = {
    "client": {
        "static_assets": STATIC_ASSETS
    },
    "server": {
        "app_config": app_config
    }
}
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC_ASSETS = os.environ.get("STATIC_ASSETS")

app_config = {
    '/': {
        'tools.sessions.on': True
    }
}

if STATIC_ASSETS:
    app_config["/"].update({'tools.staticdir.root': "/code/blog/client"})
    app_config.update({
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    })

SETTINGS = {
    "client": {
        "static_assets": STATIC_ASSETS or "https://storage.googleapis.com/michaelgreendev/client/static"
    },
    "blog": {
        "app_config": app_config
    }
}

COLORS = {}
with open(os.path.join(HERE, "colors.txt")) as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("#"):
            key = line
            COLORS[key] = []
        elif line and key:
            COLORS[key].append(line)

# for key, value in COLORS_INVERTED.items():
#     for v in value:
#         COLORS[v] = key
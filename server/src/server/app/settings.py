import os

SETTINGS = {
    "client": {
        "static_assets": os.environ.get("STATIC_ASSETS") or "https://storage.googleapis.com/michaelgreendev/client/static"
    }
}
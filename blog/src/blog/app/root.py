import os

import cherrypy
import requests

from jinja2 import Template

from .utils import templates
from ..settings import SETTINGS

class Root:
    @cherrypy.expose
    def index(self):
        with open(templates()) as f:
            template = Template(f.read())
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"]
        )
        return render

################################################################################

#  import os

# import cherrypy

# HERE = os.path.dirname(os.path.abspath(__file__))
# BLOG_ROOT = os.path.abspath(os.path.join(HERE, '../../../docs'))


# def _append_nodes(base, root=BLOG_ROOT):
#     names = os.listdir(root)
#     for name in names:
#         full_name = os.path.join(root, name)
#         if os.path.isdir(full_name):
#             setattr(base, name, Node())
#             _append_nodes(getattr(base, name), os.path.abspath(full_name))
#         elif name.endswith((".html", ".htm")):
#             base.name = full_name


# class Node:
#     @cherrypy.expose    
#     def index(self):
#         with open(self.name) as f:
#             return f.read()

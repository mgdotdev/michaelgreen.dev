import os
import random
import re
import string

import cherrypy

from datetime import datetime 

from jinja2 import Template
from markdown import markdown

from .utils import templates, docs
from ..settings import SETTINGS, COLORS

KEYWORDS_COLOR = ("#cc7832", sorted(COLORS.pop("#cc7832"), key=len, reverse=True))
DUNDERS_COLOR = ("#d800d8", COLORS.pop("#d800d8"))
SPECIALS_COLOR = ("#94558d", COLORS.pop("#94558d"))
BULTINS_COLOR = ("#8886c6", COLORS.pop("#8886c6"))

FUNCTION_COLOR = ("#ffc66d", COLORS.pop("#ffc66d")[0])
NUMBER_COLOR = ("#4984bb", COLORS.pop("#4984bb")[0])
STRING_COLOR = ("#a5c261", COLORS.pop("#a5c261")[0])
DECORATOR_COLOR = ("#bba722", COLORS.pop("#bba722")[0])
COMMENT_COLOR = ("#999999", "#.*?\n")


def _random_string(length=25):
    return "".join([random.choice(string.ascii_uppercase) for _ in range(length)])


def _format_code_string(snippet):
    if snippet["language"] != "python":
        return snippet["code"]
    snippet = snippet["code"]
    GREPPER = {}
    cswap = lambda color, item: f'<span style="color:{color}">' + item + '</span>'
    snippet = snippet.replace(">", "&gt;").replace("<", "&lt;")

    color, pattern = COMMENT_COLOR
    matches = re.finditer(pattern, snippet)
    for match in matches:
        item = match.group()[:-1]
        temp_string = _random_string()
        snippet = snippet.replace(item, temp_string)
        GREPPER[temp_string] = cswap(color, item)

    color, pattern = STRING_COLOR
    matches = re.finditer(pattern, snippet)
    for match in matches:
        item = match.group()
        temp_string = _random_string()
        snippet = snippet.replace(item, temp_string)
        item = item.replace('\\', '&#92')
        GREPPER[temp_string] = cswap(color, item)
        
    color, items = BULTINS_COLOR
    for item in items:
        temp_string = _random_string()
        GREPPER[temp_string] = cswap(color, item)
        snippet = re.sub(r"\b{}\b".format(item), temp_string, snippet)

    color, items = SPECIALS_COLOR
    for item in items:
        temp_string = _random_string()
        GREPPER[temp_string] = cswap(color, item)
        snippet = re.sub(r"\b{}\b".format(item), temp_string, snippet)

    color, pattern = FUNCTION_COLOR
    matches = re.finditer(pattern, snippet)
    for match in matches:
        item = match.group()[4:-1]
        temp_string = _random_string()
        GREPPER[temp_string] = cswap(color, item)
        snippet = re.sub(item, temp_string, snippet)

    color, items = KEYWORDS_COLOR
    for item in items:
        temp_string = _random_string()
        GREPPER[temp_string] = cswap(color, item)
        snippet = re.sub(r"\b{}\b".format(item), temp_string, snippet)

    color, pattern = DECORATOR_COLOR
    matches = re.finditer(pattern, snippet)
    for match in matches:
        item = match.group()
        snippet = snippet.replace(item, cswap(color, item))

    for key in list(GREPPER.keys()):
        value = GREPPER.pop(key)
        snippet = re.sub(key, value, snippet)

    color, items = DUNDERS_COLOR
    for item in items:
        temp_string = _random_string()
        GREPPER[temp_string] = cswap(color, item)
        snippet = re.sub(r"\b{}\b".format(item), temp_string, snippet)

    for key in list(GREPPER.keys()):
        value = GREPPER.pop(key)
        snippet = re.sub(key, value, snippet)

    return snippet


def _render_post(date, template, preview=False):
    with open(docs(date)) as f:
        post = f.read()
    regex = re.search("-{3}(?s:.*?)-{3}", post)
    headers = post[regex.start():regex.end()]
    post = post[regex.end():]
    code_blocks = [block for block in re.finditer("```.*?\n(?s:.*?)\n```", post)]
    for index, block in enumerate(code_blocks):
        snippet = block.group()
        language = re.search("```.*?\n", snippet).group()[3:-1]
        placeholder = "_".join(["snippet", str(index)])
        replacement = (
            f'<pre id="{language}">' if language else "<pre>"
        ) + placeholder + "</pre>"
        post = post.replace(snippet, replacement)
        snippets.append({
            "code": snippet[len(language)+4:-3],
            "language": language,
            "placeholder": placeholder
        })

    document = markdown(post)

    for snippet in snippets:
        document = document.replace(snippet["placeholder"], _format_code_string(snippet))

    blog_post = Template(document)
    blog_post = blog_post.render(static_assets=SETTINGS["client"]["static_assets"])
    header_image = re.search("<p><img(?s:.*?)/></p>", blog_post)
    image_tag = header_image.group()
    blog_post = blog_post.replace(image_tag, image_tag[3:-4])
    render = template.render(
        static_assets=SETTINGS["client"]["static_assets"],
        blog_post=blog_post
    )
    return render


def _lazyfunction(f):
    def wrapper(*args, **kwargs):
        hashable = f"{f.__name__}::{locals()}"
        if hashable not in wrapper.cache:
            wrapper.cache[hashable] = f(*args, **kwargs)
        return wrapper.cache[hashable]
    wrapper.cache = {}
    return wrapper


@_lazyfunction
def _posts_list_sorted():
    names = sorted(
        os.listdir(docs.dirname), 
        key = lambda date: datetime.strptime(os.path.splitext(date)[0], '%Y_%m_%d'),
        reverse = True
    )
    return names    


class Root:
    def __init__(self) -> None:
        self.posts = Posts()
        self.archives = Archives()

    @cherrypy.expose
    def index(self):
        with open(templates()) as f:
            template = Template(f.read())
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"]
        )
        return render


@cherrypy.popargs('date')
class Posts:
    @cherrypy.expose
    def index(self, date=None):
        with open(templates("posts")) as f:
            template = Template(f.read())
        if date:
            return _render_post(date, template)
        return template.render(
            static_assets=SETTINGS["client"]["static_assets"],
            blog_post="No Post Selected!"
        )


@cherrypy.popargs("year")
class Archives:
    def index(self, year=None):
        pass
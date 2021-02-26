import os
import random
import re
import string

import cherrypy

from datetime import datetime 
from functools import lru_cache

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


@lru_cache
def _parse_metadata(date, post=None):
    if type(date) == datetime:
        date = date.strftime("%Y_%m_%d")
    if not post:
        with open(docs(date)) as f:
            post = f.read()
    regex = re.search("-{3}(?s:.*?)-{3}", post)
    metadata = post[regex.start():regex.end()]
    post = post[regex.end():]
    return metadata, post


def _parse_introduction(date, post=None, trailing=False):
    if not post:
        _, post = _parse_metadata(date)
    lines = iter(post.splitlines())
    for line in lines:
        if line and not line.startswith(("#", "!")):
            if trailing:
                return markdown(line + "..")
            return markdown(line)


def _parse_title(date, post=None):
    if not post:
        _, post = _parse_metadata(date)
    lines = iter(post.splitlines()) 
    for line in lines:
        if line and line.startswith(("#")):
            return re.sub(r"#+? ", r"", line)


def _recent_posts_by_year(recent_posts):
    results = {}
    for post in recent_posts:
        try:
            results[str(post["date"].year)].append(post)
        except KeyError:
            results[str(post["date"].year)] = [post]
    return results


def _post_dates_by_focus(recent_posts=None, fmt=None):
    results = {}
    if not recent_posts:
        recent_posts = _recent_posts()
    for post in recent_posts:
        for key, values in post.items():
            if key != "date":
                if key not in results:
                    results[key] = {}
                for value in values:
                    if fmt:
                        p = post["date"].strftime(fmt)
                    else:
                        p = post["date"]
                    try:
                        results[key][value].append(p)
                    except KeyError:
                        results[key][value] = [p]
    return results


def _render_post(date, template, recent_posts):
    _, post = _parse_metadata(date)
    code_blocks = [block for block in re.finditer("```.*?\n(?s:.*?)\n```", post)]
    snippets = []
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
    return template.render(
        static_assets=SETTINGS["client"]["static_assets"],
        blog_post=blog_post,
        recent_posts=[{
                "date_file": post["date"].strftime("%Y_%m_%d"),
                "date_label": post["date"].strftime("%d %B %Y"),
                "title": _parse_title(post["date"])
            } for post in recent_posts]
    )



@lru_cache
def _post_datetimes():
    posts = (os.path.splitext(date)[0] for date in os.listdir(docs.dirname))
    return sorted(
        [datetime.strptime(post, '%Y_%m_%d') for post in posts],
        reverse=True
    )


def _recent_posts(length=None, year=None):
    results = []
    dates = _post_datetimes()[:length]
    if year:
        dates = [date for date in dates if date.year == int(year)]
    for date in dates:
        metadata, _ = _parse_metadata(date)
        items = metadata.splitlines()[1:-1]
        pairs = (item.split(": ") for item in items)
        as_dict = {key: value.split(', ') for (key, value) in pairs}
        as_dict.update({"date": date})
        results.append(as_dict)
    return results


def _posts_by_date(recent_posts=None, fmt=None):
    results = {}
    if not recent_posts:
        recent_posts = _recent_posts()
    for post in recent_posts:
        if fmt:
            results[post["date"].strftime(fmt)] = post
        else:
            results[post["date"]] = post
    return results


class Root:
    def __init__(self) -> None:
        self.recent_posts = _recent_posts(length=5)
        self.posts = Posts(self.recent_posts)
        self.archives = Archives(self.recent_posts)
        self.meta = Meta(self.recent_posts)

    @cherrypy.expose
    def index(self):
        with open(templates()) as f:
            template = Template(f.read())
        render = template.render(
            static_assets=SETTINGS["client"]["static_assets"],
            recent_posts=[{
                "date_file": post["date"].strftime("%Y_%m_%d"),
                "date_label": post["date"].strftime("%d %B %Y"),
                "title": _parse_title(post["date"]),
                "introduction": _parse_introduction(post["date"], trailing=True)
            } for post in self.recent_posts]
        )
        return render


@cherrypy.popargs('date')
class Posts:
    def __init__(self, recent_posts) -> None:
        self.recent_posts = recent_posts

    @cherrypy.expose
    def index(self, date=None):
        with open(templates("posts")) as f:
            template = Template(f.read())
        if date and datetime.strptime(date, "%Y_%m_%d") in _post_datetimes():
            return _render_post(date, template, self.recent_posts)
        return template.render(
            static_assets=SETTINGS["client"]["static_assets"],
            blog_post="No Post Selected!",
            recent_posts=[{
                "date_file": post["date"].strftime("%Y_%m_%d"),
                "date_label": post["date"].strftime("%d %B %Y"),
                "title": _parse_title(post["date"])
            } for post in self.recent_posts]
        )


@cherrypy.popargs("year")
class Archives:
    def __init__(self, recent_posts) -> None:
        self.recent_posts = recent_posts
        
    @cherrypy.expose
    def index(self, year=None):
        with open(templates("archives")) as f:
            template = Template(f.read())
        archives = _recent_posts_by_year(_recent_posts(year=year))
        for year in archives.keys():
            for post in archives[year]:
                post.update({
                    "date_file": post["date"].strftime("%Y_%m_%d"),
                    "date_label": post["date"].strftime("%d %B %Y"),
                    "title": _parse_title(post["date"]),
                    "introduction": _parse_introduction(post["date"], trailing=True)
                })

        return template.render(
            archives=archives,
            static_assets=SETTINGS["client"]["static_assets"],
            recent_posts=[{
                "date_file": post["date"].strftime("%Y_%m_%d"),
                "date_label": post["date"].strftime("%d %B %Y"),
                "title": _parse_title(post["date"]),
                "introduction": _parse_introduction(post["date"], trailing=True)
            } for post in self.recent_posts]
        )


@cherrypy.popargs("focus", "item")
class Meta:
    def __init__(self, recent_posts) -> None:
        self.recent_posts = recent_posts

    @cherrypy.expose
    def index(self, focus=None, item=None):
        with open(templates("meta")) as f:
            template = Template(f.read())
        foci = _post_dates_by_focus(fmt="%Y_%m_%d")
        posts = _recent_posts()
        for post in posts:
            post.update({
                "title": _parse_title(post["date"]),
                "date_label": post["date"].strftime("%d %B %Y"),
                "date_file": post["date"].strftime("%Y_%m_%d"),
            })
        posts = _posts_by_date(posts, fmt="%Y_%m_%d")

        if focus:
            for key in list(foci.keys()):
                if key != focus:
                    del foci[key]

        if item:
            for key in list(foci[focus].keys()):
                if key != item:
                    del foci[focus][key]

        return template.render(
            static_assets=SETTINGS["client"]["static_assets"],
            recent_posts=[{
                "date_file": post["date"].strftime("%Y_%m_%d"),
                "date_label": post["date"].strftime("%d %B %Y"),
                "title": _parse_title(post["date"])
            } for post in self.recent_posts],
            posts=posts,
            foci=foci
        )

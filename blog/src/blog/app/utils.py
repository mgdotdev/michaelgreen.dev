from .base import Templates

templates = Templates("/code/blog/client/templates", ".html")
docs = Templates("/code/blog/docs", ".md")


def lazyfunction(f):
    def wrapper(*args, **kwargs):
        hashable = f"{f.__name__}::{locals()}"
        if hashable not in wrapper.cache:
            wrapper.cache[hashable] = f(*args, **kwargs)
        return wrapper.cache[hashable]
    wrapper.cache = {}
    return wrapper
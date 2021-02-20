import os.path


class Templates:
    def __init__(self, node) -> None:
        self._node = os.path.normpath(node)

    def __getattr__(self, attr) -> None:
        return Templates(os.path.join(self._node, attr))

    def __call__(self, obj="index.html", *args, **kwargs) -> str:
        return os.path.join(self._node, obj)
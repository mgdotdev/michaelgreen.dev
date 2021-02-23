import os.path


class Templates:
    def __init__(self, node, ext) -> None:
        self._node = os.path.normpath(node)
        self._ext = (ext if ext.startswith(".") else "." + ext)

    def __getattr__(self, attr) -> None:
        return Templates(os.path.join(self.dirname, attr), self._ext)

    def __call__(self, obj="index", *args, **kwargs) -> str:
        name = (obj if obj.endswith(self._ext) else obj + self._ext)
        return os.path.join(
            self.dirname, name
        )

    @property
    def dirname(self):
        return self._node
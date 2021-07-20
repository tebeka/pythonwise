import logging


class defer:
    def __init__(self, *, name='defer'):
        self.name = name
        self.tasks = []

    def __enter__(self):
        return self.tasks

    def __exit__(self, typ, val, tb):
        for fn in reversed(self.tasks):
            try:
                fn()
            except Exception as err:
                logging.warning(
                    '%s: %s failed with %s', self.name, fn.__name__, err)


with defer() as d:
    d.append(lambda: print(1))
    d.append(lambda: print(2))

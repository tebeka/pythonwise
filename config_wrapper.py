class ConfigWrapper:
    def __init__(self, cfg):
        self._cfg = cfg

    def __getattr__(self, attr):
        try:
            val = self._cfg[attr]
            if isinstance(val, dict):
                val = ConfigWrapper(val)
            return val
        except KeyError:
            raise AttributeError(attr)

    def __dir__(self):
        return list(self._cfg)


# Demo
cfg = {
    'httpd': {
        'port': 8080,
        'interface': 'localhost',
    },
    'user': 'gary',
}

w = ConfigWrapper(cfg)
user = w.user
print(f'user: {user}')
port = w.httpd.port
print(f'httpd.port: {port}')

"""Environment based configuration"""

import json
import logging
from dataclasses import dataclass
from os import environ

_missing = object()
_prefix = 'c_'


@dataclass
class Var:
    value: object
    key: str
    conv: callable = None

    def __post_init__(self):
        value = environ.get(self.key)
        if value is None:
            return

        conv = self.conv or type(self.value)
        self.value = conv(value)


def __dir__():
    return [
        k[len(_prefix):]
        for k, v in globals().items()
        if k.startswith(_prefix) and isinstance(v, Var)
    ]


def __getattr__(attr):
    key = _prefix + attr
    var = globals().get(key, _missing)
    if var is _missing:
        raise AttributeError(attr)
    return var.value


# Configuration values should start with c_, everything else is ignored

c_http_port = Var(8080, 'HTTP_PORT')
c_log_level = Var(logging.INFO, 'LOG_LEVEL', lambda v: getattr(logging, v))
c_db_hosts = Var(['db1.local', 'db2.local'], 'DB_HOSTS', json.loads)

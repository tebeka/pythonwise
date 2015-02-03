'''Logging from Celery both to logstash and structured log (JSON) file.'''

# You need to install python-logstash package. Also have logstash agent and
# elasticsearch running.

# Example logstash configuration (logstash.conf):
# input {
#     udp => {
#         codec => json
#     }
# }
# output {
#     elasticsearch => {
#         host => localhost  # Point to your host
#     }
# }
# Then run "logstash/bin/logstash -f logstash.conf

from celery.utils.log import get_task_logger
import celery
import logstash

from logging.handlers import TimedRotatingFileHandler
from os import makedirs
from os.path import expanduser, isdir, join
import json
import logging

_logstash = {'host': 'localhost', 'port': 5959}
_logdir = expanduser('~/.local/log')


class CeleryAdapter(logging.LoggerAdapter):
    '''Adapter to add current task context to "extra" log fields'''
    def process(self, msg, kwargs):
        if not celery.current_task:
            return msg, kwargs

        kwargs = kwargs.copy()
        kwargs.setdefault('extra', {})['celery'] = \
            vars(celery.current_task.request)
        return msg, kwargs


class JSONFormatter(logging.Formatter):
    def format(self, record):
        obj = vars(record)

        # msg might be any Python object, make sure json doesn't blow up
        try:
            json.dumps(obj['msg'])
        except TypeError:
            obj['msg'] = repr(obj['msg'])

        # json can't dump exc_info, use default format as string
        if obj['exc_info']:
            obj['exc_info'] = self.formatException(obj['exc_info'])

        return json.dumps(obj)


def configure(logstash=None, logdir=None):
    '''Configuration settings.

    logstash is a dictionary of {'host': ..., 'port: ...}
    logdir is path to where log files are stored.
    '''
    global _logdir

    if not (logstash or logdir):
        raise ValueError('you must specify at least logstash or logdir')

    _logstash.update(logstash)
    _logdir = logdir or _logdir
    init_logdir(_logdir)  # We do it here so we'll fail close to the definition


def init_logdir(logdir):
    if not isdir(logdir):
        makedirs(logdir)


def new_jlogger(name):
    '''Return new logger which will log both to logstash and to file in JSON
    format.

    Log files are stored in <logdir>/name.json
    '''

    log = get_task_logger(name)

    handler = logstash.LogstashHandler(_logstash['host'], _logstash['port'])
    log.addHandler(handler)

    init_logdir(_logdir)
    handler = TimedRotatingFileHandler(
        '%s.json' % join(_logdir, name),
        when='midnight',
        utc=True,
    )
    handler.setFormatter(JSONFormatter())
    log.addHandler(handler)

    return CeleryAdapter(log, {})

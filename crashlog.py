'''Send email and log when there is an uncaught exception in your code
Use in your code:

    import crashlog
    crashlog.install(emails=['daffy@duck.com'])
'''

__author__ = 'Miki Tebeka <miki@mikitebeka.com>'

import sys
from smtplib import SMTP
from email.mime.text import MIMEText
from os import environ
from traceback import format_exception
from cStringIO import StringIO
from time import ctime

_EMAILS = []
_LOGFILE = None
_PREV_EXCEPTHOOK = None


def send_email(emails, program, message):
    message = MIMEText(message)
    message['Subject'] = '%s crashed' % program
    crashlog_email = 'noreply@somewhere.com'
    message['From'] = 'Crashlog <%s>' % crashlog_email

    smtp = SMTP('mailhost.somewhere.com')
    smtp.sendmail(crashlog_email, _EMAILS, message.as_string())


def format_message(type, value, traceback):
    message = StringIO()
    out = lambda m: message.write(u'%s\n' % m)

    out(ctime())
    out('== Traceback ==')
    out(''.join(format_exception(type, value, traceback)))
    out('\n== Command line ==')
    out(' '.join(sys.argv))
    out('\n== Environment ==')
    for key, value in environ.items():
        out('%s = %s' % (key, value))

    return message.getvalue()


def excepthook(type, value, traceback):
    try:
        if not (_EMAILS or _LOGFILE):
            return

        message = format_message(type, value, traceback)
        if _EMAILS:
            send_email(_EMAILS, sys.argv[0], message)

        if _LOGFILE:
            with open(_LOGFILE, 'at') as fo:
                print >> fo, message

    finally:
        if _PREV_EXCEPTHOOK:
            _PREV_EXCEPTHOOK(type, value, traceback)


def install(emails=None, logfile=None):
    global _EMAILS, _PREV_EXCEPTHOOK, _LOGFILE

    _EMAILS = emails or _EMAILS
    _LOGFILE = logfile
    _PREV_EXCEPTHOOK = sys.excepthook
    sys.excepthook = excepthook

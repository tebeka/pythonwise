import re

# passwd: 1234
# password: 1234
passwd_re = re.compile('^(passw(or)?d):.*$', re.MULTILINE)


def mask(text):
    """Mask passwords in text"""
    return passwd_re.sub(r'\1: XXXX', text)

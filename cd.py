'''Small cd context manger that changes directory for a given operation and
then resotres current directory.

Inspired by Fabric's cd context manager (http://bit.ly/PCBkIW)
'''
from os import getcwd, chdir

class cd:
    __doc__ = '''Context manager for changing directories for an operation

    >>> print(getcwd())
    {cwd}
    >>> with cd('/tmp'):
    ...     print(getcwd())
    /tmp
    >>> print(getcwd())
    {cwd}
    >>>
    '''.format(cwd=getcwd())
    def __init__(self, path):
        self.path = path
        self.back = getcwd()

    def __enter__(self):
        chdir(self.path)

    def __exit__(self, type, value, trackback):
        chdir(self.back)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

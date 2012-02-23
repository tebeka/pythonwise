class mock:
    '''Super simple mocking context manager.
        Example::

            import foo
            from cStringIO import StringIO
            from mock import mock

            def test_get_data():
                expected = 'Mary had a little lamb'
                with mock(foo, 'urlopen', lambda url: StringIO(expected)):
                    result = foo.get_data('http://google.com')
                assert result == expected, 'bad data'
    '''
    def __init__(self, obj, *args):
        '''Create mock object
            obj - Object to be mocked
            args - What to mock, can be either a list of ('attr', value) or a
                   dictionary.
        '''
        self.obj = obj
        if len(args) > 1:
            self.mocks = dict(zip(args[::2], args[1::2]))
        else:
            self.mocks = args[0]

    def __enter__(self):
        self.orig = self.obj.__dict__.copy()
        self.obj.__dict__.update(self.mocks)
        return self

    def __exit__(self, type, value, trackback):
        self.obj.__dict__.update(self.orig)

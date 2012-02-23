class mock:
    '''Super simple mocking context manager.
        Example::

            import foo
            from cStringIO import StringIO
            from mock import mock

            def test_get_data():
                expected = 'Mary had a little lamb'
                with mock(foo, urlopen=lambda url: StringIO(expected)):
                    result = foo.get_data('http://google.com')
                assert result == expected, 'bad data'
    '''
    def __init__(self, obj, **kw):
        '''Create mock object
            obj - Object to be mocked
            kw - Mocked attributes
        '''
        self.obj = obj
        self.mocks = kw.copy()

    def __enter__(self):
        self.orig = self.obj.__dict__.copy()
        self.obj.__dict__.update(self.mocks)
        return self

    def __exit__(self, type, value, trackback):
        self.obj.__dict__.update(self.orig)

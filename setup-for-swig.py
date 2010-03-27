from distutils.core import setup, Extension

setup(
    ext_modules = [
        Extension("_hello", sources=["hello.c", "hello.i"])
    ]
)

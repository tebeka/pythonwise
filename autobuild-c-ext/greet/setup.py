from distutils.core import Extension, setup

MODULE_NAME = "_greet"
DYNLIB = MODULE_NAME + ".so"
SRC_FILE = MODULE_NAME + ".c"

if __name__ == "__main__":
    setup(ext_modules=[Extension(MODULE_NAME, [SRC_FILE])])

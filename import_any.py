from types import ModuleType

def import_any(path, name=None):
    module = ModuleType(name or "dummy")
    execfile(path, globals(), module.__dict__)

    return module

if __name__ == "__main__":
    m = import_any("/tmp/b.foo", "b")
    print m.a
    print m.foo(2)


from types import ModuleType

def import_any(path, name=None):
    module = ModuleType(name or "dummy")
    execfile(path, globals(), module.__dict__)

    return module

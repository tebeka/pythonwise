import importlib
from sys import version_info

if version_info[:2] < (3, 6):
    raise SystemExit('error: Python 3.6+ required')

missing = []
pkgs = (
    ('jupyterlab', 'jupyterlab'),
    ('matplotlib', 'matplotlib'),
    ('pandas', 'pandas'),
    ('sklearn', 'scikit-learn'),
)

for mod, pkg in pkgs:
    try:
        importlib.import_module(mod)
    except ImportError:
        missing.append(pkg)

if not missing:
    print('You have all the requirement')
    raise SystemExit()

missing = ', '.join(sorted(missing))
print('error: you are missing the following modules - {}'.format(missing))

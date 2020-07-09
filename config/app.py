import config

for key in dir(config):
    val = getattr(config, key)
    print(f'{key} → {val}')

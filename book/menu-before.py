menu = {}


def register(fn):
    """Register function to menu"""
    menu[fn.__name__] = fn
    return fn


def copy():
    """Copy text"""
    print('>>> COPY <<<')


def paste():
    """Paste text"""
    print('>>> PASTE <<<')


# Register menu functions
register(copy)
register(paste)


def ui_loop():
    """Runs the UI loop"""
    while True:
        print('=== Menu ===')
        print('\n'.join(sorted(menu)))
        name = input('# ').strip()  # Use raw_input in Python 2
        if name == 'quit':
            break
        fn = menu.get(name)
        if not fn:
            print('ERROR: Unknown action - {}'.format(name))
            continue
        fn()

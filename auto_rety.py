
def auto_retries(fn):
    '''Automatically retry task up to config.<task_name>.max_retries

    If config.<task_name>.max_retries is not present, does nothing.
    '''
    attr = '{}.max_retries'.format(fn.__module__, fn.func_name)
    max_retries = getattr(config, attr, 0)
    if max_retries == 0:
        return fn

    @wraps(fn)
    def wrapper(*args, **kw):
        if not celery.current_task:
            return fn(*args, **kw)

        celery.current_task.max_retries = max_retries
        try:
            return fn(*args, **kw)
        except Exception as exc:
            celery.current_task.retry(exc=exc)

    return wrapper

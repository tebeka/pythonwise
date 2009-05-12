def do_something_with_data(key, data):
    open("/tmp/%s" % key, "wb").write(data)


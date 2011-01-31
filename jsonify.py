from functools import wraps
import json
from cherrypy import response, expose

def jsonify(func):
    '''JSON decorator for CherryPy'''
    @wraps(func)
    def wrapper(*args, **kw):
        value = func(*args, **kw)
        response.headers["Content-Type"] = "application/json"
        return json.dumps(value)

    return wrapper

def example():
    from cherrypy import quickstart
    from datetime import datetime
    class Time:
        @expose
        @jsonify
        def index(self):
            now = datetime.now()
            return {
                "date" : now.strftime("%Y-%m-%d"),
                "time" : now.strftime("%H:%M"),
                "day" : now.strftime("%A"),
            }

    quickstart(Time())

if __name__ == "__main__":
    example()

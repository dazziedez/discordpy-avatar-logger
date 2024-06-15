from flask import render_template
from werkzeug.exceptions import HTTPException
from werkzeug.routing.exceptions import BuildError

error_map = {
    400: {"name": "Bad Request", "description": "Oops! Your request is as broken as my heart."},
    401: {"name": "Unauthorized", "description": "You shall not pass! Authentication required."},
    403: {"name": "Forbidden", "description": "Nope, not allowed. This area is off-limits."},
    404: {"name": "Not Found", "description": "Where did it go? We couldn't find what you're looking for."},
    405: {"name": "Method Not Allowed", "description": "Wrong turn! This method isn't allowed here."},
    500: {"name": "Internal Server Error", "description": "Whoops! Something went terribly wrong on our end."},
    502: {"name": "Bad Gateway", "description": "The gateway is having a bad day. Try again later."},
    503: {"name": "Service Unavailable", "description": "We're overloaded. Give us a moment to catch our breath."},
    504: {"name": "Gateway Timeout", "description": "The gateway timed out. Maybe it fell asleep."},
}


class Error:
    def __init__(self, name, code, description):
        self.name = name
        self.code = code
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "description": self.description
        }


def handle_error(e):
    if isinstance(e, HTTPException):
        status_code = e.code
        error_info = error_map.get(status_code, {
                                   "name": "Unknown Error", "description": "An unknown error occurred."})
    elif isinstance(e, BuildError):
        status_code = 500
        error_info = {"name": "Build Error",
                      "description": "URL build error. Please contact me!! x~x"}
    else:
        status_code = 404
        error_info = error_map.get(status_code, {
                                   "name": "Unknown Error", "description": "An unknown error occurred."})

    error = Error(name=error_info["name"], code=status_code,
                  description=error_info["description"])
    return render_template('error.html', error=error.to_dict()), status_code

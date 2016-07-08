"""Base handler."""
import webapp2
import os
import jinja2
import json
from password import make_secure_val
from password import check_secure_val
from models import User

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    """Provides convenience functions for rendering templates and strings."""

    def write(self, *a, **kw):
        """Writes to page."""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Takes a string as parameter finds the matching jinja template."""
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """Renders the jinja template with the given parameters."""
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """Sets a secure cookie header with hashing."""
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            "%s=%s; Path=/" % (name, cookie_val)
        )

    def read_secure_cookie(self, name):
        """Verifies that a cookie is secure."""
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        """Logs a user in and sets a secure cookie for future use."""
        self.set_secure_cookie('user_id', str(user.key.id()))

    def logout(self):
        """Overwrites current cookie to be empty."""
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """Reads if there is any set cookies and sets them"""
        """to a global user object."""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.get_user_by_id(int(uid))

    def handle_error(request, response, exception):
        """Error handler for HTTP errors."""
        if request.path.startswith('/json'):
            response.headers.add_header('Content-Type', 'application/json')
            result = {
                'status': 'error',
                'status_code': exception.code,
                'error_message': exception.explanation,
              }
            response.write(json.dumps(result))
        else:
            response.write(exception)
            response.set_status(exception.code)

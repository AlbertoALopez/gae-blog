"""Base handler."""
import webapp2
import os
import jinja2
from app.views.utilities.password import make_secure_val, check_secure_val
from app.models.models import User

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    """Provides convenience functions common to all routing handlers."""

    def write(self, *a, **kw):
        """Writes to page."""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Takes a string as parameter finds the matching jinja template."""
        t = JINJA_ENV.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """Renders template and given paramaters to page."""
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
        """Reads if there is any cookies and sets a global user object."""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.get_user_by_id(int(uid))

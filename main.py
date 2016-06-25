"""Simple routing and rendering example using GAE with jinja2 templates."""

import os
import webapp2
import jinja2
from google.appengine.ext import ndb

# TODO: Create posts, display all posts, edit posts, delete posts, user control


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    """Base handler."""

    def write(self, *a, **kw):
        """Writes given arguments to page"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Matches given string to jinja2 template"""
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """Renders template"""
        self.write(self.render_str(template, **kw))


class Posts(ndb.Model):
    post_title = ndb.StringProperty(required=True)
    post_submitter = ndb.StringProperty()
    post_id = ndb.IntegerProperty()
    post_created = ndb.DateTimeProperty(auto_now_add=True)
    post_body = ndb.TextProperty(required=True)

    @classmethod
    def return_posts_desc(self):
        """Returns a list of descending posts."""
        posts = ndb.gql("SELECT * FROM Posts ORDER BY post_created DESC")
        return posts


class MainPage(Handler):
    """Handler for main blog page."""
    def get(self):
        posts = Posts.return_posts_desc()
        self.render("blog.html", posts=posts)


class NewPost(Handler):
    """Handler for new blog post page"""

    def render_page(self):
        self.render("newpost.html")

    def get(self):
        self.render_page()

    def post(self):
        self.render_page()

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainPage),
    webapp2.Route('/newpost', NewPost)], debug=True)

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
    # TODO: Add conditional error string

    def render_page(self, post_title="",
                    post_body="",
                    error_message=""):
        self.render("newpost.html",
                    post_title=post_title,
                    post_body=post_body,
                    error_message=error_message)

    def get(self):
        self.render_page()

    def post(self):
        post_title = self.request.get("post-title")
        post_body = self.request.get("post-body")

        if post_title and post_body:
            post = Posts(post_title=post_title, post_body=post_body)
            post.put()

            self.redirect("/")

        else:
            # Bootstrap alert error
            error_message = """<div class="alert alert-danger" role="alert" class="error-message">Please enter a post title and a post body.</div>"""
            self.render_page(error_message=error_message,
                             post_title=post_title, post_body=post_body)

    # def newline(self):
    # def validate_title:
    # def validate_body:

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainPage),
    webapp2.Route('/newpost', NewPost)], debug=True)

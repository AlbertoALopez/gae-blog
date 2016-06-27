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
    """Main handler."""

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

# blog


def blog_key(name="default"):
    return ndb.Key('blogs', name)

class Posts(ndb.Model):
    post_title = ndb.StringProperty(required=True)
    post_body = ndb.TextProperty(required=True)
    post_submitter = ndb.StringProperty()
    post_created = ndb.DateTimeProperty(auto_now_add=True)
    last_edited = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def return_posts_desc(self):
        """Returns a list of descending posts."""
        posts = ndb.gql("SELECT * FROM Posts ORDER BY post_created DESC LIMIT 10")
        return posts


class MainPage(Handler):
    """Handler for main blog page."""
    def get(self):
        posts = Posts.return_posts_desc()
        self.render("blog.html", posts=posts)

class PostPage(Handler):
    """Looks up individual posts"""
    def get(self, post_id):
        key = ndb.Key('Posts', int(post_id), parent=blog_key())
        post = key.get()
        
        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)

class NewPost(Handler):
    """Handler for new blog post page"""

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
            post = Posts(parent=blog_key(),
                         post_title=post_title,
                         post_body=post_body)
            post.put()

            self.redirect("/blog/%s" % str(post.key.id()))

        else:
            # Bootstrap alert error
            error_message = """<div class="alert alert-danger" role="alert" class="error-message">Please enter a post title and a post body.</div>"""
            self.render_page(error_message=error_message,
                             post_title=post_title, post_body=post_body)

    # def newline(self):
    # def validate_title:
    # def validate_body:

app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', PostPage)], debug=True)

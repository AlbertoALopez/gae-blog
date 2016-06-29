"""A multi user blog using GAE with jinja2 templates."""
import webapp2
from models import Posts
from BaseHandler import Handler
from NewPostHandler import NewPost
from GetPostHandler import GetPost
from FormHandler import FormHandler
from LoginHandler import LoginHandler
from WelcomeHandler import WelcomeHandler
from LogoutHandler import LogoutHandler


class MainPage(Handler):
    """Handler for main blog page."""

    def get(self):
        posts = Posts.return_posts_desc()
        self.render("blog.html", posts=posts)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', GetPost),
    ('/blog/signup', FormHandler),
    ('/blog/welcome', WelcomeHandler),
    ('/blog/login', LoginHandler),
    ('/blog/logout', LogoutHandler)], debug=True)

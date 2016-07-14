"""A multi user blog using GAE with jinja2 templates."""

import webapp2
from models import Posts
from BaseHandler import Handler
from PostHandler import NewPost, LikePost, EditPost, DeletePost
from GetPostHandler import GetPost
from FormHandler import FormHandler
from LoginHandler import LoginHandler
from WelcomeHandler import WelcomeHandler
from LogoutHandler import LogoutHandler
from CommentHandler import NewComment, LikeComment, EditComment, DeleteComment


class MainPage(Handler):
    """Handler for main blog page."""

    def get(self):
        posts = Posts.return_posts_desc()
        user = None
        if self.user:
            user = self.user
        self.render("blog.html", posts=posts, user=user)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog/signup', FormHandler),
    ('/blog/welcome', WelcomeHandler),
    ('/blog/login', LoginHandler),
    ('/blog/logout', LogoutHandler),
    ('/blog/newcomment', NewComment),
    ('/blog/likecomment', LikeComment),
    ('/blog/editcomment', EditComment),
    ('/blog/deletecomment', DeleteComment),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', GetPost),
    ('/blog/likepost', LikePost),
    ('/blog/editpost', EditPost),
    ('/blog/deletepost', DeletePost)], debug=True)

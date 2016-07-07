"""Handler that retrieves individual posts."""
from BaseHandler import Handler
from google.appengine.ext import ndb
from models import blog_key
from models import Comments


class GetPost(Handler):
    """Looks up individual posts."""

    def get(self, post_id):
        postkey = ndb.Key('Posts', int(post_id), parent=blog_key())
        post = postkey.get()
        user = None
        comments = Comments.return_comments(post_id)

        if self.user:
            user = self.user
        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, user=user, comments=comments)

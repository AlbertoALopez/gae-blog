"""Handler that retrieves individual posts."""
from BaseHandler import Handler
from google.appengine.ext import ndb
from models import blog_key


class GetPost(Handler):
    """Looks up individual posts."""

    def get(self, post_id):
        key = ndb.Key('Posts', int(post_id), parent=blog_key())
        post = key.get()

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)

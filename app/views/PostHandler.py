"""Handler for posts."""

from google.appengine.ext import ndb
from BaseHandler import Handler
from app.models.models import Posts, blog_key
import bleach


class NewPost(Handler):
    """Handler for new blog post page."""

    def render_page(self, post_title="",
                    post_body="",
                    error_message=""):
        user = None
        if self.user:
            user = self.user
        self.render("newpost.html",
                    post_title=post_title,
                    post_body=post_body,
                    error_message=error_message,
                    user=user)

    def get(self):
        """Handler for GET requests."""
        self.render_page()

    def post(self):
        """Handler for POST requests."""
        # If a request maker is not a valid user, throw unauthorized error
        if not self.user:
            self.error(401)
            self.render('error.html', error=401)
            return

        post_title = self.request.get("post-title")
        post_body = self.request.get("post-body")
        post_submitter = self.request.get("post-submitter")
        post_category = self.request.get("post-category")

        if post_title and post_body:
            post = Posts(parent=blog_key(),
                         post_title=post_title,
                         post_body=post_body,
                         post_submitter=post_submitter,
                         post_category=post_category)
            print(post_body.encode('utf-8'))
            post.put()

            self.redirect("/blog/%s" % str(post.key.id()))

        else:
            # Bootstrap alert error
            error_message = """<div class="alert alert-danger"
                role="alert" class="error-message">Please enter a post title
                and a post body.</div>"""
            self.render_page(error_message=error_message,
                             post_title=post_title, post_body=post_body)


class LikePost(Handler):
    """Handler for post likes."""

    def put(self):
        """Handler for PUT requests."""
        # If a valid user did not make request, throw unauthorized error
        if not self.user:
            self.error(401)
            self.render('error.html', error=401)
            return

        post_id = self.request.get("post-id")
        post_liker = int(self.request.get("post-liker"))
        post = Posts.return_post(post_id)

        # If post exists, increment and return
        if post and self.user.name != post.post_submitter:
            if post.post_likes is None:
                post.post_likes = 1

            else:
                post.post_likes += 1
                post.put()

            # If user has already liked post do not add again to list
            for post_liker in post.liked_by:
                if post_liker == post_liker:
                    post.put()
                    return

            post.liked_by.append(int(post_liker))
            post.put()

        else:
            self.error(500)
            self.render('error.html', error=500)


class EditPost(Handler):
    """Handler for general post edits."""

    def get(self, post_id):
        if not self.user:
            self.error(401)
            self.render('error.html', error=401)
            return

        postkey = ndb.Key('Posts', int(post_id), parent=blog_key())
        post = postkey.get()
        user = None

        # Check if request is authorized
        if self.user.name == post.post_submitter:
            user = self.user
        else:
            self.error(401)
            self.render('error.html', error=401)
            return

        # If post does not exist
        if not post:
            self.error(404)
            self.render('error.html', error=404)
            return

        self.render("editpost.html", post=post, user=user)

    def put(self, user):
        """Handler for PUT requests."""
        if not self.user:
            self.error(401)
            self.render('error.html', error=401)
            return

        post_id = self.request.get("post-id")
        post_body = self.request.get("post-body")
        post = Posts.return_post(post_id)

        if post and self.user.name == post.post_submitter:
            post.post_body = post_body
            post.put()

        else:
            self.error(500)
            self.render('error.html', error=500)

    def post(self, user):
        """Handler for POST requests."""
        if not self.user:
            self.error(401)
            self.render('error.html', error=401)
            return

        post_id = self.request.get("post-id")
        post_title = bleach.clean(self.request.get("post-title"), strip=True)
        post_body = self.request.get("post-body")
        post_category = self.request.get("post-category")
        post = Posts.return_post(post_id)

        if post and self.user.name == post.post_submitter:
            post.populate(
                post_title=post_title,
                post_body=post_body,
                post_category=post_category
            )
            post.put()
            self.redirect("/blog/%s" % str(post.key.id()))

        else:
            self.error(500)
            self.render('error.html', error=500)


class DeletePost(Handler):
    """Handler for post deletion."""

    def put(self):
        """Handler for PUT requests."""
        if not self.user:
            self.error(401)
            self.render('error.html', error=401)
            return
        post_id = self.request.get("post-id")
        post_key = ndb.Key('blogs', 'default', 'Posts', int(post_id))
        post = post_key.get()

        if post_key and self.user.name == post.post_submitter:
            post_key.delete()

        else:
            self.error(500)
            self.render('error.html', error=500)

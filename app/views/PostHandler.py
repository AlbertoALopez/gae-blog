"""Handler for new posts created."""
from BaseHandler import Handler
from models import Posts
from models import blog_key
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
        self.render_page()

    def post(self):
        post_title = bleach.clean(self.request.get("post-title"), strip=True)
        post_body = bleach.clean(self.request.get("post-body"), strip=True)
        post_submitter = self.request.get("post-submitter")
        post_category = self.request.get("post-category")

        if post_title and post_body:
            post = Posts(parent=blog_key(),
                         post_title=post_title,
                         post_body=post_body,
                         post_submitter=post_submitter,
                         post_category=post_category)
            post.put()

            self.redirect("/blog/%s" % str(post.key.id()))

        else:
            # Bootstrap alert error
            error_message = """<div class="alert alert-danger" role="alert" class="error-message">Please enter a post title and a post body.</div>"""
            self.render_page(error_message=error_message,
                             post_title=post_title, post_body=post_body)


class PostLiked(Handler):
    """Handler for post likes."""

    def put(self):
        """Handler for PUT requests."""
        post_id = self.request.get("post-id")
        post_liker = int(self.request.get("post-liker"))
        post = Posts.return_post(post_id)

        # If post exists, increment and return
        if post:
            if post.post_likes is None:
                post.post_likes = 1

            else:
                post.post_likes = post.post_likes + 1
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


class PostEdit(Handler):
    """Handler for post edits."""

    def put(self):
        """Handler for PUT requests."""
        post_id = self.request.get("post-id")
        post_body = self.request.get("post-body")
        post = Posts.return_post(post_id)

        if post:
            post.post_body = post_body
            post.put()

        else:
            self.error(500)


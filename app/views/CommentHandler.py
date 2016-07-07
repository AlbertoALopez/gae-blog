"""Handler for new comments."""
from BaseHandler import Handler
from models import Comments


class NewComment(Handler):
    """Handler for new comment."""

    def post(self):
        comment_parent_id = self.request.get("comment-parent-id")
        comment_submitter = self.request.get("comment-submitter")
        comment_body = self.request.get("comment-body")

        if comment_body and comment_submitter:
            comment = Comments(
                         parent=int(comment_parent_id),
                         comment_submitter=comment_submitter,
                         comment_body=comment_body)
            comment.put()

        else:
            # Bootstrap alert error
            error_message = """<div class="alert alert-danger" role="alert" class="error-message">There was an error submitting your comment.</div"""
            self.render('/', error_message)

"""Handlers for comments."""

from google.appengine.ext import ndb
from BaseHandler import Handler
from app.models.models import Comments
import json


class NewComment(Handler):
    """Handler for new comment."""

    def post(self):
        """Handle POST requests."""
        parent = int(self.request.get("parent"))
        comment_submitter = self.request.get("comment-submitter")
        comment_body = self.request.get("comment-body")

        if comment_body and comment_submitter:
            comment = Comments(
                         parent=int(parent),
                         comment_submitter=comment_submitter,
                         comment_body=comment_body)
            comment.put()

            comment_id = comment.key.id()

            # Output json to AJAX response
            self.response.headers['Content-Type'] = 'application/json'
            json_obj = {
                'commentSubmitter': comment_submitter,
                'commentBody': comment_body,
                'parent': parent,
                'id': comment_id
            }
            self.response.out.write(json.dumps(json_obj))


class LikeComment(Handler):
    """Handler for new comment likes."""

    def put(self):
        """Handle PUT requests."""
        comment_id = self.request.get("comment-id")
        comment_liker = int(self.request.get("comment-liker"))
        comment = Comments.return_comment(comment_id)

        # If comment exists, increment and return
        if comment:
            if comment.comment_likes is None:
                comment.comment_likes = 1

            else:
                comment.comment_likes += 1
                comment.put()

            # If user has already liked comment do not add again to list
            for comment_liker in comment.liked_by:
                if comment_liker == comment_liker:
                    comment.put()
                    return

            comment.liked_by.append(int(comment_liker))
            comment.put()

        # Else render HTTP error message
        else:
            self.error(500)


class EditComment(Handler):
    """Handler for comment edits."""

    def put(self):
        """Handle PUT requests."""
        comment_id = self.request.get("comment-id")
        comment_body = self.request.get("comment-body")
        comment = Comments.return_comment(comment_id)

        if comment:
            comment.comment_body = comment_body
            comment.put()

        else:
            self.error(500)


class DeleteComment(Handler):
    """Handler for comment deletion."""

    def put(self):
        """Handle PUT requests."""
        comment_id = self.request.get("comment-id")
        comment_key = ndb.Key('Comments', int(comment_id))

        if comment_key:
            comment_key.delete()

        else:
            self.error(500)

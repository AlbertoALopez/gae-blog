"""Handler for new comments."""
from BaseHandler import Handler
from models import Comments
import json


class NewComment(Handler):
    """Handler for new comment."""

    def post(self):
        parent = self.request.get("parent")
        comment_submitter = self.request.get("comment-submitter")
        comment_body = self.request.get("comment-body")

        if comment_body and comment_submitter:
            comment = Comments(
                         parent=int(parent),
                         comment_submitter=comment_submitter,
                         comment_body=comment_body)
            comment.put()

            # Output json to AJAX response
            self.response.headers['Content-Type'] = 'application/json'
            jsonObj = {
                'commentSubmitter': comment_submitter,
                'commentBody': comment_body,
                'parent': parent,
                'penis': 'penis'
            }
            self.response.out.write(json.dumps(jsonObj))

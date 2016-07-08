"""Database models."""
from google.appengine.ext import ndb
from password import make_pw_hash
from password import valid_pw


def blog_key(name="default"):
    """Returns blog key."""
    return ndb.Key('blogs', name)


def users_key(group='default'):
    key = ndb.Key('users', group)
    return key


class User(ndb.Model):
    """Database model for a user object."""

    name = ndb.StringProperty(required=True)
    hashed_pw = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    @classmethod
    def get_user_by_id(CLASS, uid):
        """Retrieves user object by its id."""
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def get_user_by_name(CLASS, name):
        """Retrieves user object by its name."""
        user = User.query(User.name == name).get()
        return user

    @classmethod
    def register(CLASS, name, password, email=None):
        """Registers a new user."""
        hashed_pw = make_pw_hash(name, password)
        return User(parent=users_key(),
                    name=name,
                    hashed_pw=hashed_pw,
                    email=email)

    @classmethod
    def user_login(CLASS, name, password):
        """Verifies that a user can login."""
        user = CLASS.get_user_by_name(name)
        if user and valid_pw(name, password, user.hashed_pw):
            return user


class Posts(ndb.Model):
    """NDB model for Posts entity."""

    post_title = ndb.StringProperty(required=True)
    post_body = ndb.TextProperty(required=True)
    post_submitter = ndb.StringProperty()
    post_created = ndb.DateTimeProperty(auto_now_add=True)
    post_category = ndb.StringProperty()
    post_likes = ndb.StringProperty()
    last_edited = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def return_posts_desc(CLASS):
        """Returns a list of descending posts."""
        posts = ndb.gql("SELECT * FROM Posts ORDER BY post_created DESC LIMIT 10")
        return posts


class Comments(ndb.Model):
    """NDB model for Comment entity."""

    comment_submitter = ndb.StringProperty(required=True)
    comment_body = ndb.TextProperty(required=True)
    comment_created = ndb.DateTimeProperty(auto_now_add=True)
    comment_likes = ndb.IntegerProperty()
    parent = ndb.IntegerProperty()
    liked_by = ndb.IntegerProperty(repeated=True)

    @classmethod
    def return_comments(CLASS, parent_id):
        """Returns all comments in store that have the given parent."""
        comments = Comments.query(Comments.parent == int(parent_id)).order(Comments.comment_created).fetch()
        return comments

    @classmethod
    def return_comment(CLASS, comment_id):
        """Return comment with specific id."""
        key = ndb.Key('Comments', int(comment_id))
        comment = key.get()
        return comment

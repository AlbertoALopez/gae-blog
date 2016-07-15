"""Password helper functions."""
import hmac
import hashlib
import random
import string
from secret import SECRET


def make_salt(length=5):
    """Makes a random salt of 5 characters."""
    return ''.join(random.choice(string.letters) for x in range(length))


def make_pw_hash(name, password, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + password + salt).hexdigest()
    return "%s, %s" % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def hash_str(s):
    """Hashes a string produced with hmac."""
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    """Returns a string of format s,HASH."""
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    """Checks if the given hash is secure and valid."""
    string = h.split('|')[0]
    if h == make_secure_val(string):
        return string
    else:
        return None

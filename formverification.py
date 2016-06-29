"""Convenience functions for form verification."""
import re

USER_RE = re.compile(r"[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    """Returns true if matches a valid username"""
    return username and USER_RE.match(username)


def valid_password(password):
    """Returns true if matches valid password"""
    return password and PASSWORD_RE.match(password)


def verify_password(first_password, verify):
    """Returns true if both passwords match"""
    return first_password and verify and first_password == verify


def valid_email(email):
    """Returns true if matches valid email"""
    return not email or EMAIL_RE.match(email)

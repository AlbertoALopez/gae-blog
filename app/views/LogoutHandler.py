"""Logs the user out and redirects to the signup page."""
from BaseHandler import Handler


class LogoutHandler(Handler):
    def get(self):
        self.logout()
        self.redirect('/')

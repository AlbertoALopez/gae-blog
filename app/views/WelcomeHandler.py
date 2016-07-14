"""Handler for valid form redirect."""
from BaseHandler import Handler


class WelcomeHandler(Handler):
    """Verifies if there is a valid user signed in and redirects."""
    def get(self):
        if self.user:
            user = self.user
            self.render('welcome.html', user=user)
        else:
            self.redirect('/blog/signup')

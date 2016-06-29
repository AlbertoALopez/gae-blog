"""Handler for valid form redirect."""
from BaseHandler import Handler


class WelcomeHandler(Handler):
    """Verifies if there is a valid user signed in and redirects."""
    def get(self):
        if self.user:
            # Render page with valid username
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/blog/signup')

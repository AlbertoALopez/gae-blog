"""Handler for the login page."""
from BaseHandler import Handler
from utilities.formverification import *
from app.models.models import User


class LoginHandler(Handler):
    """Handler for login page."""

    def form_verified(self):
        if User.user_login(self.user_name, self.user_password):
            user = User.get_user_by_name(self.user_name)
            self.login(user)
            self.redirect('/blog/welcome')
        else:
            error_message = "User does not exist. Please signup."
            self.render("signup.html", error_message=error_message)

    def get(self):
        if self.user:
            self.redirect('/blog/welcome')
        self.render('login.html')

    def post(self):
        # Request username and password from form
        self.user_name = self.request.get('username')
        self.user_password = self.request.get('password')
        # Generate error message if invalid username or password
        username_error = "" if valid_username(self.user_name) else "Please enter a valid username."
        password_error = "" if valid_password(self.user_password) else "Please enter a valid password."

        if username_error == "" and password_error == "":
            # Form is verified and redirect to welcome
            self.form_verified()
        else:
            self.render('login.html',
                        username_error=username_error,
                        password_error=password_error)

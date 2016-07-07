"""Creates a signup page with rudimentary validation and redirection."""
from BaseHandler import Handler
from models import User
from formverification import *


class FormHandler(Handler):
    def form_verified(self):
        """Called when form is verified."""
        # Make sure user doesn't already exist
        user = User.get_user_by_name(self.user_name)
        if user:
            message = "That user already exists."
            self.render('signup.html', error_username=message)
        else:
            # Create user object in database
            user = User.register(
                self.user_name,
                self.user_password,
                self.user_email)
            user.put()

            # Log the user in and redirect to welcome page
            self.login(user)
            self.redirect('/blog/welcome')

    def get(self):
        user = None
        if self.user:
            user = self.user
        self.render("signup.html", user=user)

    def post(self):
        """Validates user input and return errors if tests fail"""
        self.user_name = self.request.get("username")
        self.user_password = self.request.get("password")
        self.user_verify = self.request.get("verify")
        self.user_email = self.request.get("email")

        # Error messages
        username_error = "" if valid_username(self.user_name) else "Please enter a valid username."
        password_error = "" if valid_password(self.user_password) else "Please enter a valid password."
        verify_error = "" if verify_password(self.user_password, self.user_verify) else "Your passwords do not match."
        email_error = "" if valid_email(self.user_email) else "That's not a valid email."
        # If there are no error messages
        if username_error == "" and password_error == "" and verify_error == "":
            # Call method done() and redirect to welcome
            self.form_verified()

        else:
            # Otherwise re render form
            self.render('signup.html',
                        username_error=username_error,
                        password_error=password_error,
                        verify_error=verify_error,
                        email_error=email_error)

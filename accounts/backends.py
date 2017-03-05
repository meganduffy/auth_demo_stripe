"""
Here we create a class that with replace the standard 'auth' object that Django
uses to check logins, and override twi default methods.

The authenticate method finds the user by email address and checks the password
We've simply swapped the username field for the email field

We have overridden the get_user method to show that you can apply extra conditions
to the login process.
We're simply making sure a user is active and whether they can log in
This is ideal for a user ban or disabling accounts

In settings.py -> AUTHENTICATION_BACKENDS = (
                        'django.contrib.auth.backends.ModelBackend',
                        'accounts.backends.EmailAuth',
                )
"""
from models import User


class EmailAuth(object):
    def authenticate(self, email=None, password=None):
        """
        Get an instance of User using the supplied email and check its password
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Used by the django authentication system to retrieve an instance of User
        """
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None

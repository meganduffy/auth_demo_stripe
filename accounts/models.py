"""
We import AbstractUser and UserManager
Abstract user contains a basic set of attributes for our User model
like is_superuser and is_active to set default permissions
UserManager is the class you access when you type User.objects
It handles things like creating normal and superuser accounts
when you register someone new

In settings.py -> AUTH_USER_MODEL = 'accounts.User'
"""
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
import datetime


class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    # Now that we've abstracted this class we can add any number
    # Of custom attributes to our user class
    stripe_id = models.CharField(max_length=40, default='')
    last_login = models.DateTimeField(default=timezone.now)
    m = datetime.datetime(year=2016, month=01, day=01)
    previous_login = models.DateTimeField(default=m)
    objects = AccountUserManager()



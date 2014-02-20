"""Custom user model for DjangoDevs. Also, has functionality for merging user
accounts.
"""

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import URLValidator
from django.db import models
from hashlib import md5
from utils.fields.model_fields import CurrencyField, UsernameField
from utils.urls import reverse_url

import random

GITHUB = 1
GOOGLE = 2
MEETUP = 3
STACKEXCHANGE = 4

def generate_username():
    """Randomly generates a username, similar to stackoverflow. This provides
    a sample space of 89,999,999 possible outcomes.
    """
    while True:
        new_user_id = "user-" + str(random.randrange(10000000, 99999999))
        try:
            user = DjangoDev.objects.get(username=new_user_id)
        except DjangoDev.DoesNotExist:
            return new_user_id

def generate_gravatar(username, size=128):
    """Generates an identicon gravatar of whatever size specified. The default
    is 128x128 pixels. Returns the gravatar url is successful, or None
    otherwise.
    """
    hashed_text = md5(username.encode('utf-8')).hexdigest()
    return "https://secure.gravatar.com/avatar/%s?s=%s&d=identicon&r=pg" % (
        hashed_text, size
    )

class DjangoDevManager(BaseUserManager):
    """Model manager for DjangoDev models."""

    def create_user(self, username, password=None):
        """Creates a new user. If there is no password, then an OAuth account
        is assumed to be used here. The password will be set to '0' if that is
        the case.
        """
        if not username:
            username = generate_username()
        image = generate_gravatar(username)
        user = self.model(username=username, image=image)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """Creates an administrator user."""
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class DjangoDev(AbstractBaseUser):
    """Custom Django User"""
    username = UsernameField(max_length=65, unique=True, db_index=True)
    job_title = models.CharField(max_length=75, blank=True, null=True)
    company = models.CharField(max_length=75, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    image = models.TextField(validators=[URLValidator()])
    is_company = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects = DjangoDevManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.username

    def change_username(self, name):
        """Changes the username of a DjangoDev."""
        self.username = name

    def get_full_name(self):
        """Required by django, returns username"""
        return self.username

    def get_short_name(self):
        """Required by django, returns username"""
        return self.username

    def has_perm(self, perm, obj=None):
        """Manage permissions for site administrators"""
        return True

    def has_module_perms(self, app_label):
        """Determines whether an admin can view the settings for an app"""
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_url(self):
        return reverse_url('user-detail', args=[self.username])

    def get_accounts(self):
        """Returns a list of attached accounts used by oauth"""
        return self.accounts.all()

    def get_posts(self):
        """Returns a list of all blog posts made"""
        return self.blog_posts.all()

class OAuthAccount(models.Model):
    """Model for attaching user accounts from oauth providers to DjangoDev
    users.
    """
    ACCOUNT_TYPES = (
        (GITHUB, 'github'),
        (GOOGLE, 'google'),
        (MEETUP, 'meetup'),
        (STACKEXCHANGE, 'stackexchange')
    )

    user = models.ForeignKey(DjangoDev, related_name='accounts')
    username = models.CharField(max_length=255) # From the provider
    account_type = models.IntegerField(
        max_length=1,
        choices=ACCOUNT_TYPES)

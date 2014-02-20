"""
Urls for /oauth/
"""

from django.conf.urls import (patterns, url)
from .views import (
    GithubOAuthCallback, GoogleOAuthCallback,
    MeetupOAuthCallback, StackexchangeOAuthCallback)

urlpatterns = patterns('',
    url(r'github/$', GithubOAuthCallback.as_view(), name="github-login"),
    url(r'google/$', GoogleOAuthCallback.as_view(), name="google-login"),
    url(r'meetup/$', MeetupOAuthCallback.as_view(), name="meetup-login"),
    url(r'stackexchange/$',
        StackexchangeOAuthCallback.as_view(), name="stackexchange-login")
)

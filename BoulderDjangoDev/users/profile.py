from django.conf.urls import patterns, url
from .views import UserProfile

urlpatterns = patterns('',
    url(r'^$', UserProfile.as_view(), name="user-profile"),
)

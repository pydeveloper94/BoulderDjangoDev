from django.conf.urls import patterns, url
from .views import UserProfile

urlpatterns = patterns('',
    url(r'^(?P<username>[A-z0-9\-\_\.]+)/$', UserProfile.as_view(), 
        name='user-detail'),
)

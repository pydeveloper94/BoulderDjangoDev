from django.conf.urls import patterns, url
from .views import LogoutUser

urlpatterns = patterns('',
    url(r'^$', LogoutUser.as_view(), name="logout"),
)

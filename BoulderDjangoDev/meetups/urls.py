from django.conf.urls import patterns, url
from .views import MeetupList

urlpatterns = patterns('',
    url(r'^$', MeetupList.as_view(), name="blog-list")
)

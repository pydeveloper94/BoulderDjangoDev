"""Defines all of the urls under /blog/"""

from django.conf.urls import patterns, url
from .views import BlogList, BlogListUser, BlogDetail, CommentList, CommentEdit
#, CommentList, CommentEdit

urlpatterns = patterns('',
    url(r'^$', BlogList.as_view(), name="blog-list"),
    url(r'^(?P<username>[A-z0-9\-\_\.]+)/$', BlogListUser.as_view(), 
        name="user-blog-list"),
    url(r'^(?P<username>[A-z0-9\-\_\.]+)/(?P<title_slug>[\w-]+)/$',
        BlogDetail.as_view(), name="blog-detail"),
    url(r'^(?P<username>[A-z0-9\-\_\.]+)/(?P<title_slug>[\w-]+)/comments/$',
        CommentList.as_view(), name="comment-list"),
    url(r'^(?P<username>[A-z0-9\-\_\.]+)/(?P<title_slug>[\w-]+)'
        '/comments/(?P<pk>\d+)/$', CommentEdit.as_view(), name="comment-edit")
)

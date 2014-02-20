from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

## Custom functionality while initializing the server
from utils.managers import initialize_processes
initialize_processes()

urlpatterns = patterns('',
    url(r'^home/', include('home.urls')),
    url(r'^oauth/', include('oauth.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^meetups/', include('meetups.urls')),
    url(r'^logout/', include('users.logout')),
    url(r'^users/', include('users.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls))
)

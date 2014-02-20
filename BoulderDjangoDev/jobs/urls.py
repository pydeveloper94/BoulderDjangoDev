"""Defines the urls under /jobs/"""

from django.conf.urls import patterns, url
from .views import JobList, JobDetail, JobCompanyList, RenewJob

urlpatterns = patterns('',
    url(r'^$', JobList.as_view(), name="job-list"),
    url(r'^(?P<pk>\d+)/$',
        JobDetail.as_view(), name="job-detail"),
    url(r'^(?P<pk>\d+)/renew/$',
        RenewJob.as_view(), name="renew-job"),
    url(r'^(?P<company_slug>[A-z0-9\-\_\.]+)/$', 
        JobCompanyList.as_view(), name="job-company-list"),
)

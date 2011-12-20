#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.conf.urls.defaults import patterns, include
from django.contrib import admin
admin.autodiscover()

from blog import urls as blogUrls

urlpatterns = patterns('',
  (r'^sentry/', include('sentry.web.urls')),
  (r'^admin/', include(admin.site.urls)),
  (r'^', include(blogUrls)),
)

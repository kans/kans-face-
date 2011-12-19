#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.conf.urls.defaults import patterns, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from blog import urls as blogUrls

urlpatterns = patterns('',
  (r'^sentry/', include('sentry.web.urls')),
  (r'^', include(blogUrls)),
)

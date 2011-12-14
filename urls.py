#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.conf.urls.defaults import patterns, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import blog.urls

urlpatterns = patterns('',
 (r'^$', include(blog.urls)),
)

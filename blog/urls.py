#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from blog import views

urlpatterns = patterns('',

  (r'^/(?P<slug>.*)/$', views.lookup_article),
  (r'^$', views.splash),
)

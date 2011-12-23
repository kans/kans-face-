#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.conf.urls.defaults import patterns, include

from blog import views

urlpatterns = patterns('',
  (r'^ckeditor/', include('ckeditor.urls')),
  (r'^archives$', views.archives),
  (r'^$', views.splash),
  (r'^comments/', include('django.contrib.comments.urls')),
  (r'^make-comment/', views.ajax_comment),
  (r'^post/(?P<slug>.*)$', views.lookup_article),
)

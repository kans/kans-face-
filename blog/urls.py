#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.conf.urls.defaults import patterns, include, url

from blog import views

urlpatterns = patterns('',
  (r'^ckeditor/', include('ckeditor.urls')),
  url(r'^feed$', views.Feeder(), name="feeder"),
  (r'^archives$', views.archives),
  (r'^$', views.splash),
  (r'^comments/', include('django.contrib.comments.urls')),
  (r'^make-comment/(\d*)', views.ajax_comment),
  (r'^get-recent-posts', views.get_recent_posts),
   url(r'^post/(?P<slug>.*)$', views.lookup_article, name="lookup-article"),
)

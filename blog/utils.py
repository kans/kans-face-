#!/usr/bin/python
#Copyright 2011 Matt Kaniaris
""" some handy utils and stuff that doesn't belong anywhere really """

from django.template.loader import render_to_string

from blog import models

def _filter_articles():
  """ I got tired of writing this everywhere """
  #pylint: disable = E1101
  return models.Article.objects.filter(is_live=True).order_by('-updated_on')

def render_recent_posts():
  recentPosts =  _filter_articles().values("slug", "title")[:5]
  return render_to_string('recent-posts.html', {'posts': recentPosts })



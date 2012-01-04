#!/usr/bin/python
#Copyright 2011 Matt Kaniaris
""" some handy utils and stuff that doesn't belong anywhere really """

from django.template.loader import render_to_string

from blog import models

def render_recent_posts():
  recentPosts =  models.Article.filter_live().values("slug", "title")[:5]
  return render_to_string('recent-posts.html', {'posts': recentPosts })



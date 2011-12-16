#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django import template

from blog import models

register = template.Library()

class GetRecentPosts(template.Node):
  def __init__(self, number=5):
    self.number = number

  def render(self, context):
    articles = models.Article.filter('-updated_at').values('slug')[:5]
    return [a.to_href for a in articles]

  @staticmethod
  def get_recent_posts(number):
    return GetRecentPosts(number)



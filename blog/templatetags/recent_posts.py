#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django import template

from blog import models

register = template.Library()

class GetRecentPosts(template.Node):
  def __init__(self, contextName, number=5):
    self.number = number
    self.contextName = contextName

  def render(self, context):
    context[self.contextName] =  models.Article.objects.filter(is_live=True).order_by('-updated_on')[:5]
    return ""

  @staticmethod
  def get_recent_posts(parser, token):
    try:
      # split_contents() knows not to split quoted strings.
      tagName, number, string, contextName = token.split_contents()
    except ValueError:
      name = token.contents.split()[0]
      raise template.TemplateSyntaxError("use %r tag as such: %r num as var" % (name, name))
    try:
      number = int(number)
    except ValueError:
      raise template.TemplateSyntaxError("use %r tag as such: %r num as var" % (name, name))
    return GetRecentPosts(contextName, number)

register.tag('recent_stuffs', GetRecentPosts.get_recent_posts)


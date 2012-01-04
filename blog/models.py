#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.db import models
from django.db.models.signals import post_save

import baseModels

class Article(baseModels.BaseModel):
  """ a blog article """
  title = models.TextField(help_text="The title of the article")
  body = models.TextField(help_text="The content of the article")
  slug = models.TextField(help_text="Article slug")
  is_live = models.BooleanField(help_text="Is this article visible to the public?", default=False)

  @staticmethod
  def filter_live(**kwargs):
    """ I got tired of writing this everywhere """
    #pylint: disable = E1101
    return Article.objects.filter(is_live=True, **kwargs).order_by('-updated_on')

  @models.permalink
  def get_absolute_url(self):
    return ('lookup-article', (), {'slug': self.slug})

  @property
  def url(self):
    return self.get_absolute_url()

  class Meta:
    app_label = 'blog'


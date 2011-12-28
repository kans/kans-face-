#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.db import models
from django.contrib.auth import models as authModels

import baseModels

class Article(baseModels.BaseModel):
  """ a blog article """
  title = models.TextField(help_text="The title of the article")
  body = models.TextField(help_text="The content of the article")
  slug = models.TextField(help_text="Article slug")
  is_live = models.BooleanField(help_text="Is this article visible to the public?", default=False)

  @models.permalink
  def get_absolute_url(self):
    return ('lookup-article', (), {'slug': self.slug})

  @property
  def url(self):
    return self.get_absolute_url()

  class Meta:
    app_label = 'blog'

class Comment(baseModels.BaseModel):
  """ a comment on an Article """
  body = models.TextField(help_text="the comment...")
  article = baseModels.SafeForeignKey(Article)
  user = baseModels.SafeForeignKey(authModels.User)


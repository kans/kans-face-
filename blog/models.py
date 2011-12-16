#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.db import models

import baseModels

class Article(baseModels.BaseModel):
  """ a blog article """
  title = models.TextField(help_text="The title of the article")
  body = models.TextField(help_text="The content of the article")
  slug = models.TextField(help_text="Article slug")
  date = models.TextField(help_text="The date the article was written")

  @models.permalink
  def get_absolute_url(self):
    return ('lookup_article', (), {'slug': self.slug})

  @property
  def url(self):
    return self.get_absolute_url()

class Comment(baseModels.BaseModel):
  """ a comment on an Article """
  body = models.TextField(help_text="the comment...")
  article = models.ForeignKey(Article)


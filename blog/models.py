#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.db import models
from django.core.urlresolvers import reverse

import baseModels

class Article(baseModels.BaseModel):
  title = models.TextField(help_text="The title of the article")
  body = models.TextField(help_text="The content of the article")
  slug = models.TextField(help_text="Article slug")
  date = models.TextField(help_text="The date the article was written")

  def to_href(self):
    return reverse('lookup_article', args=(self.slug,))

class Comment(baseModels.BaseModel):
  body = models.TextField(help_text="the comment...")
  article = models.ForeignKey(Article)


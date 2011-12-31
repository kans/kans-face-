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

  @models.permalink
  def get_absolute_url(self):
    return ('lookup-article', (), {'slug': self.slug})

  @property
  def url(self):
    return self.get_absolute_url()

  class Meta:
    app_label = 'blog'

  @staticmethod
  def post_save(sender, instance, **kwargs):
    """Don't fail silently or do clobber a test.
    Note, we can't use a unique constraint because we want to allow any number of inactive tests with a shared goal"""

    sharedGoals = ABTest.objects.filter(goal=instance.goal, active=True)
    if sharedGoals:
      raise ValueError("We can't tell these tests apart: %s: %s and the one you tried to create. Set the old one to inactive or change the goal of this one." % (sharedGoals[0].name, sharedGoals[0].id))


post_save.connect(Article.post_save, sender=Article)

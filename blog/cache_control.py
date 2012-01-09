#!/usr/bin/python
#Copyright 2011 Matt Kaniaris
""" handles updating some cached objects/renderings after we receive the appropriate signals"""


from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.dispatch import receiver

from blog import models

#: the time left before the timeout when we consider the object stale
CACHE_EPSILON_TIMEOUT = 60

def cache_control(f):
  def wrapper(request, *args, **kwargs):
    # don't cache stuff for logged in users
    if not request.user.is_anonymous():
      return f(request, *args, **kwargs)



def update_recent_posts_cache():
  recentPosts =  models.Article.filter_live().values("slug", "title")[:5]
  response = render_to_string('recent-posts.html', {'posts': recentPosts })
  key = reverse('blog.views.get_recent_posts')
  cache.set(key, response, 60*60*24*7)
  return response

@receiver(post_save, sender=models.Article)
def recent_posts_receiever(sender, **kwargs):
  """ simple receiver to update our cache for recent posts after any article
  has been saved.  We will update a bit too frequently, but how often
  do you write blog articles?"""
  #TODO: implement caching of pages after I get sleep

  instance = kwargs['instance']

  if kwargs['created'] or instance.is_live:
    update_recent_posts_cache()
    cache.set(SPLASH_SLUG, instance.slug)



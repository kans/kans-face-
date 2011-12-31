#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.http import HttpResponse
from django.core.cache import cache
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from blog import models
from blog.cache_control import update_recent_posts_cache
from blog.utils import _filter_articles

def lookup_article(request, slug):
  article = get_object_or_404(models.Article, slug=slug, is_live=True)
  context = RequestContext(request)
  context['article'] = article
  return render_to_response("article.html", context)

def get_recent_posts(request):
  """ returns the rendered list of links to posts as a ul """
  # is this a good idea?
  key = request.path
  # should make a wrapper to do this that takes the key and time
  response = cache.get(key, None)
  if response is not None:
    return HttpResponse(response)
  freshResponse = update_recent_posts_cache()
  return HttpResponse(freshResponse)

def splash(request):
  articles = _filter_articles().values('slug', 'created_on', 'updated_on')
  return render_to_response("blog-index.html", {'articles': articles})

class _article(object):
  def __init__(self, **kwargs):
    for key,value in kwargs.items():
      setattr(self, key, value)

  def time(self):
    #pylint: disable = E1101
    return self.created_on.strftime('%b %d')

def archives(request):
  """ returns a page renderning links to all posts ever """
  # its easier to maintain some app level sql sorting than making a monster query I think?
  articles = _filter_articles().values('slug', 'created_on', 'title')
  dates = {}
  for article in articles:
    time = article['created_on']
    year = time.year
    dates.setdefault(year, [])
    dates[year].append(_article(**article))

  return render_to_response("archives.html", {'dates': dates})

def ajax_comment(request, articleID):
  """ returns the comment-form in a whole webpage """
  article = get_object_or_404(models.Article, id=articleID, is_live=True)
  context = {}
  context.update(csrf(request))
  context.update(article=article)
  return render_to_response("comment-form.html", context)



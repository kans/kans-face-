#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

"""Views for the blog.  Also, an experiment in using full paths"""

import django.http
import django.core.cache
import django.core.context_processors
import django.template
import django.shortcuts

import blog.models
import blog.cache_control

def lookup_article(request, slug):
  article = django.shortcuts.get_object_or_404(blog.models.Article, slug=slug, is_live=True)
  context = django.template.RequestContext(request)
  context['article'] = article
  return django.shortcuts.render_to_response("article.html", context)

def get_recent_posts(request):
  """ returns the rendered list of links to posts as a ul """
  # is this a good idea?
  key = request.path
  # should make a wrapper to do this that takes the key and time
  response = django.core.cache.cache.get(key, None)
  if response is not None:
    return django.http.HttpResponse(response)
  freshResponse = blog.cache_control.update_recent_posts_cache()
  return django.http.HttpResponse(freshResponse)

def splash(request):
  response = django.core.cache.cache.get('splash.html', None)
  if response is not None:
    return django.http.HttpResponse(response)
  slug = django.core.cache.cache.get('splash.slug', None)
  if slug is not None:
    return lookup_article(request, slug)
  articles = blog.models.Article.filter_live().values('slug')
  slug = articles[0]['slug']
  return lookup_article(request, slug)

class _article(object):
  """ convenience object for representing some limited parts of a blog.blog.models.Article """
  def __init__(self, **kwargs):
    for key,value in kwargs.items():
      setattr(self, key, value)

  def time(self):
    #pylint: disable = E1101
    return self.created_on.strftime('%b %d')

def archives(request):
  """ returns a page renderning links to all posts ever """
  # its easier to maintain some app level sql sorting than making a monster query I think?
  articles = blog.models.Article.filter_live().values('slug', 'created_on', 'title')
  dates = {}
  for article in articles:
    time = article['created_on']
    year = time.year
    dates.setdefault(year, [])
    dates[year].append(_article(**article))

  return django.shortcuts.render_to_response("archives.html", {'dates': dates})

def ajax_comment(request, articleID):
  """ returns the comment-form in a whole webpage """
  article = django.shortcuts.get_object_or_404(blog.models.Article, id=articleID, is_live=True)
  context = {}
  context.update(django.core.context_processors.csrf(request))
  context.update(article=article)
  return django.shortcuts.render_to_response("comment-form.html", context)



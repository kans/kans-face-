#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response

from blog import models

def lookup_article(request, slug):
  article = get_object_or_404(models.Article, slug=slug, is_live=True)
  context = {}
  context.update(csrf(request))
  context.update(article=article)
  return render_to_response("article.html", context)

def splash(request):
  articles = models.Article.objects.filter(is_live=True).order_by('-created_on').values('slug', 'created_on', 'updated_on')
  return render_to_response("blog-index.html", {'articles': articles})
class _article(object):
  def __init__(self, slug, created_on, title):
    self.created_on = created_on
    self.slug = slug
    self.title = title

  def time(self):
    return self.created_on.strftime('%b %d')

def archives(request):
  """ returns a page renderning links to all posts ever """
  # its easier to maintain some app level sql sorting than making a monster query I think?
  articles = models.Article.objects.filter(is_live=True).order_by('-created_on').values('slug', 'created_on', 'title')
  dates = {}
  for article in articles:
    time = article['created_on']
    year = time.year
    dates.setdefault(year, [])
    dates[year].append(_article(**article))

  return render_to_response("archives.html", {'dates': dates})

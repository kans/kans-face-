#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string
from blog import models

def lookup_article(request, slug):
  article = get_object_or_404(models.Article, slug=slug, is_live=True)
  return render_to_response("article.html", {'article': article})

def splash(request):
  articles = models.Article.objects.filter(is_live=True).order_by('-created_on').values('slug', 'created_on', 'updated_on')
  return render_to_response("blog-index.html", {'articles': articles})

class _article(object):
  def __init__(self, **kwargs):
    for key,value in kwargs.items():
      setattr(self, key, value)

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

#@csrf_protect
def ajax_comment(request, articleID):
  if request.method == "POST":
    from django.contrib.comments.views import comments
    response = comments.post_comment(request, next=None, using=None)
    return response
  article = get_object_or_404(models.Article, id=articleID, is_live=True)
  context = {}
  context.update(csrf(request))
  context.update(article=article)
  return render_to_response("comment-form.html", context)



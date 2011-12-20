#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.shortcuts import get_object_or_404, render_to_response

from blog import models

def lookup_article(request, slug):
  article = get_object_or_404(models.Article, slug=slug, is_live=True)
  return render_to_response("article.html", {'article': article})

def splash(request):
  articles = models.Article.objects.filter(is_live=True).order_by('-created_on').values('slug', 'created_on', 'updated_on')
  return render_to_response("blog-index.html", {'articles': articles})

def archives(request):
  """ returns a page renderning links to all posts ever """
  # its easier to maintain some app level sql sorting than making a monster query I think?
  articles = models.Article.objects.filter(is_live=True).order_by('-created_on').values('slug', 'date_published', 'updated_on')
  dates = {}
  for article in articles:
    if article.date_published.year not in dates:
      dates[article.date_published.year] = []

  return render_to_response("archives.html", {'articles': articles})

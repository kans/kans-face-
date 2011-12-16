#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

from django.shortcuts import get_object_or_404, render_to_response

from blog import models

def lookup_article(request, slug):
  article = get_object_or_404(models.Article, slug=slug)
  return render_to_response("article.html", {'article': article})

def splash(request):
  articles = models.Article.order_by('-created_on').values('slug', 'created_on', 'updated_on')
  return render_to_response("blog-index.html", {'articles': articles})

#!/usr/bin/python
#Copyright 2011 Matt Kaniaris

"""Views for the blog.  Also, an experiment in using full paths"""

import django.http
import django.core.cache
cache = django.core.cache.cache
import django.core.urlresolvers
import django.core.context_processors
import django.template
import django.template.loader
import django.shortcuts
import django.dispatch
import django.views.decorators.cache
import django.db.models.signals
import django.contrib.syndication.views

import blog.models
import blog.utils


class Feeder(django.contrib.syndication.views.Feed):
  """ Handles rss feed """
  title = "kan'sface latest"
  link = ""

  def items(self):
    return blog.models.Article.filter_live()[0:1]

  def item_title(self, article):
    return article.title

  def item_description(self, article):
    return article.slug

def render_article(request, slug):
  article = django.shortcuts.get_object_or_404(blog.models.Article, slug=slug, is_live=True)
  context = django.template.RequestContext(request)
  context['article'] = article
  return django.template.loader.render_to_string("article.html", context)

@django.views.decorators.cache.never_cache
def lookup_article(request, slug):
  """ returns a blog article
  NOTE: we accept sprinkling cache stuff in this view and this view only because
  it is so easy to do in this case because there is no need to worry about
  everything it touches.  This is probably a premature optimization and caching this page could
  be handled using the timeout method employed elsewhere."""

  #try cache first if anon
  useCache = request.user.is_anonymous()
  if useCache:
    key = request.path
    response = cache.get(key, None)
    if response is not None:
      return django.http.HttpResponse(response)

  response = render_article(request, slug)
  if useCache:
    cache.set(key, response, 60*60*24*7)
  return django.http.HttpResponse(response)

@django.dispatch.receiver(django.contrib.comments.signals.comment_was_flagged)
@django.dispatch.receiver(django.contrib.comments.signals.comment_was_posted)
def recent_comment_receiver(sender, comment, request, **kwargs):
  """ handles updating the cache when we get a new comment """
  modelInstance = comment.content_object
  django.db.models.signals.post_save.send(sender=blog.models.Article, instance=modelInstance)

@django.dispatch.receiver(django.db.models.signals.post_save, sender=blog.models.Article)
def recent_posts_receiever(sender, **kwargs):
  """ simple receiver to update our cache for recent posts after any article
  has been saved.  We will update a bit too frequently, but how often
  do you write blog articles?"""
  instance = kwargs['instance']
  #NOTE: Temporary hack since render_article raises a 404 if the article isn't live
  if not instance.is_live:
    return
  key = django.core.urlresolvers.reverse(lookup_article, kwargs={'slug':instance.slug})
  fakeRequest = django.http.HttpRequest()
  articleHTML = render_article(fakeRequest, instance.slug)
  cache.set(key, articleHTML, 60*60*24*7)

@django.views.decorators.cache.cache_control(max_age=60*5)
def get_recent_posts(request):
  """ returns the rendered list of links to posts as a ul """
  recentPosts =  blog.models.Article.filter_live().values("slug", "title")[:5]
  response = django.template.loader.render_to_string('recent-posts.html', {'posts': recentPosts })
  return django.http.HttpResponse(response)

@django.views.decorators.cache.never_cache
def splash(request):
  """ handles caching of the splash page"""
  response = cache.get('splash.html', None)
  if response is not None:
    return django.http.HttpResponse(response)
  slug = cache.get('splash.slug', None)
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

@django.views.decorators.cache.never_cache
def ajax_comment(request, articleID):
  """ returns the comment-form in a whole webpage """
  article = django.shortcuts.get_object_or_404(blog.models.Article, id=articleID, is_live=True)
  context = {}
  context.update(django.core.context_processors.csrf(request))
  context.update(article=article)
  return django.shortcuts.render_to_response("comment-form.html", context)

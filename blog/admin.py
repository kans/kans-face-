#!/usr/bin/python
#Copyright 2011 Matt Kaniaris
"""Django admin interface specification"""

from django import forms
from django.contrib import admin
from django.core import urlresolvers
from django.utils.safestring import mark_safe
from django.utils.html import escape

from ckeditor.widgets import CKEditorWidget

from blog import models

class ModelLinkWidget(forms.HiddenInput):
  """ Replaces drop down boxes with a link to the damn thing instead"""
  def __init__(self, adminSite, originalObject):
    self.adminSite = adminSite
    self.originalObject = originalObject
    super(ModelLinkWidget,self).__init__()

  def render(self, name, value, attrs=None):
    if not self.originalObject:
      return "None?"

    # pylint: disable = W0212
    link = urlresolvers.reverse('admin:%s_%s_change' % (self.originalObject._meta.app_label, self.originalObject._meta.module_name),
                         args=(self.originalObject.id,))

    return super(ModelLinkWidget, self).render(name, value, attrs) + \
      mark_safe('<a href="%s">%s</a>' % (link, escape(unicode(self.originalObject))))


class ModelLinkAdmin(admin.ModelAdmin):
  """ Use me to replace drop down boxes of foreign keys to links to them:
  add a model_link attr to the model to point the way
  NOTE: you can not use model_link and readonly_fields!
  """
  date_hierarchy = 'created_on'
  readonly_fields = ('updated_on', 'created_on', 'id')
  date_hierarchy = 'created_on'
  model_link = ()

  def __init__(self, *args, **kwargs):
    conflict = set(self.readonly_fields).intersection(set(self.model_link))
    assert not conflict, "Go remove '%s' from readonly_fields or model_links for %s" % (" ".join([x for x in conflict]), self.__class__.__name__)
    super(ModelLinkAdmin, self).__init__(*args, **kwargs)

  def get_form(self, request, obj=None):
    form = super(ModelLinkAdmin, self).get_form(request, obj)

    # bail if we are making a new object or if we dont' have a model link
    if request.META['PATH_INFO'][-5:] == '/add/' or not hasattr(self, 'model_link'):
      return form

    for field_name in self.model_link:
      if field_name in form.base_fields:
        originalObject = getattr(obj, field_name, None)
        form.base_fields[field_name].widget = ModelLinkWidget(self.admin_site, originalObject)
        form.base_fields[field_name].required = False
    return form

class PostArticleForm(forms.ModelForm):
  body = forms.CharField(widget=CKEditorWidget())

  class Meta:
    model = models.Article

class ArticleAdmin(ModelLinkAdmin):
  model_link = ( )
  list_filter = ( 'created_on', 'is_live',  )
  list_display = ( 'id', 'slug', 'is_live', 'created_on', 'title')
  form = PostArticleForm

admin.site.register(models.Article, ArticleAdmin)

class CommentAdmin(ModelLinkAdmin):
  model_link = ('article', )
  list_filter = ( 'article', 'created_on', 'user')
  list_display = ( 'id', 'created_on', 'user' )

admin.site.register(models.Comment, CommentAdmin)

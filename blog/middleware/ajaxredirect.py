from django.http import HttpResponseRedirect

class AjaxRedirect(object):
  """ returns a 278 instead of having 302s followed by ajax calls """
  def process_response(self, request, response):
    if request.is_ajax():
      if type(response) == HttpResponseRedirect:
        response.status_code = 278
    return response


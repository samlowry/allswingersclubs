#-*- coding: utf8 -*-

"""
RENDER_TO DECORATOR
"""
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
	    response = output
            if isinstance(output, (list, tuple)):
                response = render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                response = render_to_response(template, output, RequestContext(request))
	    
	    """
	    MY CODE FOR SETTING COOKIE
	    """
	    if 'cookie_key' in output and 'cookie_days' in output:
		response.set_cookie( key=output.get('cookie_key',''),
				    value=unicode(output.get('cookie_value','')).encode('utf8'),
				    max_age=int(output.get('cookie_days','0'))*86400,
				    expires=datetime.datetime.now() + datetime.timedelta(days=output.get('cookie_days','0')),
				    path='/', domain=None, secure=None)
            return response
        return wrapper
    return renderer



"""
URL DECORATOR
"""
import sys

from django.core.urlresolvers import RegexURLResolver
from django.conf.urls.defaults import patterns

def url(*args):
	"""
	Usage:
	@url(r'^users$')
	def get_user_list(request):
		...
		
	@url(r'^info/$', r'^info/(.*)/$') # will match both
	@render_to('wiki.html')
	def wiki(request, title=''):
		...
	"""
	caller_filename = sys._getframe(1).f_code.co_filename
	module = None
	for m in sys.modules.values():
		if m and '__file__' in m.__dict__ and m.__file__.startswith(caller_filename):
			module = m
			break
	def _wrapper(f):
		if module:
			if 'urlpatterns' not in module.__dict__:
				module.urlpatterns = []
			for pattern in args:
				module.urlpatterns += patterns('',(pattern,f))
		return f
	return _wrapper

def include_urlpatterns(regex, module):
	"""
	Usage:
	
	# in top-level module code:
	urlpatterns = include_urlpatterns(r'^profile/', 'apps.myapp.views.profile')
	"""
	return [RegexURLResolver(regex, module)]

from django import template
from linkator.models import Tradelink

register = template.Library()

class TradelinksNode(template.Node):
	def __init__(self, var_name):
		self.var_name = var_name

	def render(self, context):
		request = context['request']
		context[self.var_name] = Tradelink.objects.filter(page__path__exact=request.path).order_by('id')
		return ''

import re
#@register.tag
def get_tradelinks(parser, token):
	try:
		tag_name, arg = token.contents.split(None, 1)
	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
	m = re.search(r'as (\w+)', arg)
	if not m:
		raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
	var_name, = m.groups()
	return TradelinksNode(var_name)

register.tag(get_tradelinks)
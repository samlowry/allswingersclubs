from django import template
from django.template.defaultfilters import stringfilter
# from django.utils.encoding import force_unicode, iri_to_uri
from django.utils.safestring import mark_safe, SafeData

register = template.Library()

import re

@register.filter
@stringfilter
def my_slugify(value):
    """
    Normalizes string, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '-', value).strip())
    return mark_safe(re.sub('[-\s]+', '-', value))
my_slugify.is_safe = True
my_slugify = stringfilter(my_slugify)


register.filter(my_slugify)
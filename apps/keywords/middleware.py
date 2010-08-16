import urlparse
import cgi
import re

from django.http import HttpResponseRedirect
from keywords.models import Keyword

class KeywordMiddleware(object):
    PARAMS = {
        'google': 'q',
        'search\.yahoo': 'p', 
        '(search\.msn|w*\.bing)?': 'q',
        'search\.live': 'query',
        'search\.aol': 'userQuery', # maybe 'q' ?
        'ask\.com': 'q', 
        'altavista': 'q',
        'feedster': 'q',
        'search\.lycos\.': 'query',
        'w*\.{0,1}alltheweb': 'q', 
        'yandex': 'text',
        '(nova\.|search\.)?rambler\.': 'query',
        'gogo\.': 'q',
        'go\.mail\.': 'q'
    }
    @classmethod
    def parse_search(cls, url):
        try:
            parsed = urlparse.urlsplit(url)
            loc_net = parsed[1]
            query = parsed[3]
        except (AttributeError, IndexError):
            return None
        for engine, param in cls.PARAMS.iteritems():
            match = re.match(engine, loc_net)
            if match:
                keywords = cgi.parse_qs(query).get(param)
                if keywords and keywords[0]:
                    keywords = " ".join(keywords[0].split()).lower()
                    return keywords
        return None
    def process_request(self, request):
        try:            
            referer = request.META.get('HTTP_REFERER')
            keywords = self.parse_search(referer)
            if keywords:
                kw = Keyword(text=keywords)
                kw.save()
        except Exception, err:
            pass
        return None

import urlparse
import cgi
import re

from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

from keywords.models import Keyword
from keywords.models import KeywordState
 
class KeywordMiddleware(object):
    PARAMS = {
        'w*\.{0,1}google': 'q',
        'search\.yahoo': 'p', 
        'search\.msn\.': 'q',
        'w*\.{0,1}bing\.': 'q',
        'search\.live': 'query',
        'search\.aol': 'q', 
        'w*\.{0,1}ask\.com': 'q', 
        'w*\.{0,1}altavista': 'q',
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
                # print (engine, loc_net)
                keywords = cgi.parse_qs(query).get(param)
                if keywords and keywords[0]:
                    keywords = " ".join(keywords[0].split()).lower()
                    return keywords
        return None
    def process_request(self, request):
        # is the keywords turn on for current site
        if not KeywordState.state.enabled():
            # no keywords for this site 
            path = request.get_full_path()
            if path.startswith("/search/"):
                raise Http404
            return None
        try:            
            referer = request.META.get('HTTP_REFERER')
            keywords = self.parse_search(referer)
            if keywords:
                kw = Keyword(text=keywords)
                kw.save()
        except Exception, err:
            pass
        return None

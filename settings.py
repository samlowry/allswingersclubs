import os.path
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

DEBUG = False

from multisite.threadlocals import SiteIDHook
SITE_ID = SiteIDHook()

APPEND_SLASH = False

CACHE_BACKEND = 'file:///tmp/django_cache'
CACHE_MIDDLEWARE_SECONDS = 60*60*24
CACHE_MIDDLEWARE_KEY_PREFIX = SITE_ID

ADMIN_MEDIA_PREFIX = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
	os.path.join(PROJECT_ROOT, 'templates'),
)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'clubs'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = 'root'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9w+@byf8+ocnvn*!_n=@p4zhp#f-_5u#8r^8644)l3^^et4-7v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'multisite.template_loader.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
	'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.http.ConditionalGetMiddleware',
    # 'django.middleware.common.CommonMiddleware',
	'multisite.middleware.DynamicSiteMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	'django.middleware.cache.FetchFromCacheMiddleware',	
    
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.request',
	'context_processors.get_current_site_id',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.flatpages',
    'django.contrib.admin',
	'django.contrib.sitemaps',
    'django.contrib.comments',
	'linkator',
	'directory',
	'comments',
	'south',
    'registration',
    'news',
    'reversion',
    'tapes',
    'imagekit',
)

try:
	from local_settings import *
except ImportError:
	pass
    
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 # one year
SESSION_SAVE_EVERY_REQUEST = True
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = "webmaster@allswingresclubs.org"
ACCOUNT_ACTIVATION_DAYS = 14

AUTH_PROFILE_MODULE = 'registration.RegistrationProfile'

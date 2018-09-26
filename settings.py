import os.path
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

DEBUG = False

from multisite.threadlocals import SiteIDHook
SITE_ID = SiteIDHook()

APPEND_SLASH = False


CACHE_BACKEND = 'file:///tmp/django_cache/asc'
CACHE_MIDDLEWARE_SECONDS = 60*60*24
CACHE_MIDDLEWARE_KEY_PREFIX = SITE_ID

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache/asc',
        'TIMEOUT': 60*60*24,
        'KEY_PREFIX': SITE_ID,
    }
}

# ADMIN_MEDIA_PREFIX = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clubs',
        'USER': 'clubs',
        'PASSWORD': 'clubs123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {"init_command": "SET foreign_key_checks = 0,character_set_connection=utf8,collation_connection=utf8_unicode_ci",},
        'STORAGE_ENGINE': 'MyISAM',
    }
}

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'clubs'             # Or path to database file if using sqlite3.
DATABASE_USER = 'clubs'             # Not used with sqlite3.
DATABASE_PASSWORD = 'clubs123'         # Not used with sqlite3.
DATABASE_HOST = '127.0.0.1'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.


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
    # 'django.template.loaders.filesystem.load_template_source',
    # 'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
    #  'django.template.loaders.eggs.load_template_source',
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
    # 'django.middleware.csrf.CsrfResponseMiddleware',
    'keywords.middleware.KeywordMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'context_processors.get_current_site_id',
    'context_processors.get_all_keywords',
    'context_processors.get_current_site_flatpages',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
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
    # 'forum',
    'comments',
    'south',
    'registration',
    'news',
    'reversion',
    'tapes',
    'imagekit',
    'keywords',
    'paging',
    'extra_comments',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
COMMENTS_APP = 'extra_comments'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 # one months
SESSION_SAVE_EVERY_REQUEST = False
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = "webmaster@allswingersclubs.org"
ACCOUNT_ACTIVATION_DAYS = 14

AUTH_PROFILE_MODULE = 'registration.RegistrationProfile'
MAX_STACK_LENGTH = 10 # maximum of saved keywords for each site

try:
    from local_settings import *
except ImportError:
    pass

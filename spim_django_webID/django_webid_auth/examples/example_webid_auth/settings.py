# Django settings for webidauth project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

STATIC_URL = "/static/"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'django_webid.auth.backends.WEBIDAuthBackend',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_webid.auth.middleware.WEBIDAuthMiddleware'
)

#
# WebID-Auth Specific Settings
#

WEBIDAUTH_CREATE_USER = True

def createusercb(req):
    from build_user import build_custom_user
    return build_custom_user(req)

# FIXME use lambda here.
WEBIDAUTH_CREATE_USER_CALLBACK = createusercb
WEBIDAUTH_USE_COOKIE = True
WEBIDAUTH_LOGIN_URL = None

WEBIDAUTH_USERNAME_SPARQL = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?uri ?givenName ?familyName
WHERE {
  ?uri foaf:givenName ?givenName .
   OPTIONAL {
      ?uri foaf:familyName ?familyName .
   }
}
"""
WEBIDAUTH_USERNAME_VARS = ('uri', 'givenName', 'familyName')

ROOT_URLCONF = 'example_webid_auth.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django_webid.provider',
    'django_webid.auth'
)

# Sample Logging Config.
# Split into settings_local_example

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            #'format': '[%(levelname)s] %(asctime)s %(module)s %(process)d %(thread)d %(message)s'},
            'format': '[%(levelname)s] [%(module)s] (%(process)d, %(thread)d): %(message)s'},
        'simple': {
            'format': '[%(levelname)s] %(message)s'},
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
    },
        'console': {
            'formatter': 'simple',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'v-console': {
            'formatter': 'verbose',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
    },
        'django_webid.auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'webid': {
            'handlers': ['v-console'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}


try:
    from settings_local import *
except ImportError:
    pass

# coding: utf-8

from datetime import timedelta


# ============================
#   Django project settings
# ============================

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# The ID, as an integer, of the current site in the django_site database table.
# This is used so that application data can hook into specific site(s) and
# a single database can manage content for multiple sites.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    
    'accounts',
    'lib',
    'news',
)


# =================================
#   Application settings section
# =================================

# Accounts
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_REDIRECT_URL = '/'

# The number of days an activation link is valid for
REGISTRATION_TIMEOUT_DAYS = 3
EMAIL_CHANGE_TIMEOUT_DAYS = 3

# Period of time between two email requests for individual user
# (for now using for password reset only)
EMAIL_REQUEST_DELAY = timedelta(minutes=30)

# Community page
ACCOUNTS_PER_PAGE = 15


# News
CUT_TAG = '<!-- more -->'
LATEST_NEWS_COUNT = 5


# Pagination
#
# 1 2 ... 6 7 [8] 9 10 ... 91 92
# |_|     |_|     |__|     |___|
# tail     ^padding^        tail

PAGINATION_PADDING = 3
PAGINATION_TAIL = 2


# Import local settings depending on running environment
# See local_settings.sample for example
try:
    from local_settings import *
except ImportError:
    pass

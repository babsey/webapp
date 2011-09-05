# -*- coding: utf-8 -*-

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
    #'debug_toolbar.middleware.DebugToolbarMiddleware',    
)

#import socket
#if socket.gethostname() == 'mayflower':
  #MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'urls'

DATABASE_ROUTERS = ['lib.db_routers.AppRouter']

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
    'forum',
    'lib',
    'news',

    'django_evolution',
    'django_extensions',
    'debug_toolbar',
    'form_utils',

    'network',
    'reversion',
    'djcelery',
    'djkombu',
    'result',
)


# =================================
#   Application settings section
# =================================

#  Accounts
# ===================
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


#  Forum
# ===================
TOPICS_PER_PAGE = 10
POSTS_PER_PAGE = 10
SUBSCRIPTIONS_PER_PAGE = 15

POPULAR_TOPICS_PERIOD = timedelta(days=7)
POPULAR_TOPICS_COUNT = 7

NEW_TOPICS_COUNT = 7

TOPIC_PAGINATION_LEFT_TAIL = 3
TOPIC_PAGINATION_RIGHT_TAIL = 5

GLUE_MESSAGE_TIMEOUT = 10*60
GLUE_MESSAGE = u'\n\n[color=#BBBBBB][small]Added %s[/small] later[/color]\n%s'

FORUM_UNREAD_DEPTH = 100

FORUM_FEED_ITEMS_COUNT = 30

BBMARKUP_EXTRA_RULES = [
    {'pattern': r'\[hidden\](.*?)\[/hidden\]', 'repl': ur'<div class="hidden-header">Hidden text</div><div class="hidden-text" style="display: none">\1</div>'},
    {'pattern': r'\[hidden title=(.*?)\](.*?)\[/hidden\]', 'repl': ur'<div class="hidden-header">\1</div><div class="hidden-text" style="display: none">\2</div>'},
    {'pattern': r'\[video\]http://www\.youtube\.com/watch\?v=([a-z\d_-]+)\[/video\]', 'repl': r'<div class="video"><iframe class="youtube-player" type="text/html" width="748" height="455" src="http://www.youtube.com/embed/\1" frameborder="0"></iframe></div>'},
]


#  News
# ===================
CUT_TAG = '<!-- more -->'
LATEST_NEWS_COUNT = 5
NEWS_FEED_ITEMS_COUNT = 15


#  Pagination
# ===================

# 1 2 ... 6 7 [8] 9 10 ... 91 92
# |_|     |_|     |__|     |___|
# tail     ^padding^        tail
PAGINATION_PADDING = 3
PAGINATION_TAIL = 2


# Database connection settings
# found out that DATABASES should be in settings.py, i'dont know why
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_default',
        'USER': 'sysad',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'ssl': {
                'ca': '/path/to/cacert.pem',
                },
            },
    },

    'network': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test2_network',
        'USER': 'sysad',
        'PASSWORD': '',
    },

    'simulation': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test2_simulation',
        'USER': 'sysad',
        'PASSWORD': '',
    },
}


#  Debug Toolbar
# ===================

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    #'lib.debug_toolbar.panels.profiling.ProfilingPanel',
)

def custom_show_toolbar(request):
    return True # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    #'EXTRA_SIGNALS': ['lib.decorators.signals'],
    'HIDE_DJANGO_SQL': False,
    'TAG': 'div',
}


# Import local settings depending on running environment
# See local_settings.sample for example
try:
    from local_settings import *
except ImportError:
    pass

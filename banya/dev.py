from .settings import *

DEBUG = True

INTERNAL_IPS = ['127.0.0.1', ]

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map', r'.+\node_modules'],
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     },
#     'local': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     },
# }
#
# SOLO_CACHE = 'local'
# SOLO_CACHE_TIMEOUT = 60*5 #5 минут
# SOLO_CACHE_PREFIX = 'solo'

X_FRAME_OPTIONS = 'SAMEORIGIN'
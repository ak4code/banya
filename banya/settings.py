import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'solo',
    'import_export',
    'webpack_loader',
    'django_cleanup',
    'easy_thumbnails',
    'sitetree',
    'tinymce',
    'adminsortable',
    'rest_framework',
    'django_filters',
    'core.apps.CoreConfig',
    'store.apps.StoreConfig',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'banya.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.get_site_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'banya.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATETIME_FORMAT = "d.m.Y H:M"
DATE_FORMAT = "d.m.Y"
SHORT_DATE_FORMAT = "d.m.Y"

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

THUMBNAIL_ALIASES = {
    '': {
        'small': {'size': (100, 100), 'quality': 80, 'crop': True},
        'medium': {'size': (300, 300), 'quality': 80, 'crop': True},
    },
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'link image preview codesample contextmenu table code lists textcolor colorpicker',
    'toolbar1': 'formatselect | fontselect | forecolor | backcolor | bold italic underline | alignleft aligncenter alignright alignjustify '
                '| bullist numlist | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'statusbar': True,
    'width': 'auto',
    'height': 360,
}

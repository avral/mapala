import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SESSION_COOKIE_HTTPONLY = False

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'dbbackup',
    'rest_framework',
    'django_filters',
    'backend',
    'apps.pages',
    'apps.locomotive',
    'apps.auth_api',
    'apps.groups',
    'apps.passcode',
    'mptt',
    # 'pagedown',
    # 'tagulous',
    # 'draceditor',
    # 'steem',
]

AUTH_USER_MODEL = 'auth_api.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.auth.middleware.AuthSigHashMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'backend.middleware.LocaleMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'backups'}

SITE_ID = 1

ROOT_URLCONF = 'backend.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_PATH, '../static')
STATICFILES_DIRS = ('backend/static', )

MEDIA_ROOT = os.path.join(ROOT_PATH, '../media')
MEDIA_URL = '/media/'

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates', 'plain', 'example'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

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


AUTHENTICATION_BACKENDS = [
    'backend.authentication.EmailAsUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework.authentication.TokenAuthentication'
]


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'apps.auth_api.hasher.MyCryptoHash',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_VERIFY_EXPIRATION': False,

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.auth_api.utils.jwt_response_payload_handler',
}

APPEND_SLASH = True


GR_CAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'

# Prerender
PRERENDER_UA_REGEX = """
    Ask Jeeves|baiduspider|twitterbot|facebookexternalhit|rogerbot|linkedinbot|embedly|
    quora link preview|showyoubot|outbrain|pinterest|slackbot|vkShare|W3C_Validator|yandex|
    Telegram|Site Analyzer|SiteAnalyzerBot|Viber|Whatsapp|Telegram|
"""

# Добавелние DACom в список блокчейнов
from bitsharesbase.chains import known_chains

known_chains['DACom'] = {
    "chain_id": "526880c720c677ef7b54f964fe68999d1e582a33c8636b0f3b4687d47ae2f67f",
    "core_symbol": "FLO",
    "prefix": "FLO"
}

DACOM_NODE_WSS = 'ws://144.217.15.182:11011'

###
# Тут все конфиги которые относятся к фронтенду для блокчейна
FRONTEND_APP_NAME = 'mapala/1.0'
APP_FETCH_FROM = 'mapala'  # Тред с которым синхронизируются посты
APP_PUSH_TO = 'testing'  # Тред куда уходят посты
USER_PREFIX = 'mpl'
LOCALE = 'ru'  # По дефолту Русский язык


COMPRESS_IMAGE_QUALITY = 50  # Percentage

BLOCKCHAIN_DATABASES = {
    # базы блокчейнов
    'steemit': {
        'server': 'sql.steemsql.com',
        'database': 'DBSteem',
        'username': 'steemit',
        'password': 'steemit',
        'driver': '{ODBC Driver 13 for SQL Server}'
    },
    'golos': {
        'server': 'sql.golos.cloud',
        'database': 'DBGolos',
        'username': 'golos',
        'password': 'golos',
        'driver': '{ODBC Driver 13 for SQL Server}'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mapala_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/mapala.log',
            'formatter': 'verbose',
        },
        'django_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'dacom_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/dacom.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['django_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'mapala': {
            'handlers': ['mapala_file', 'console'],
            'level': 'INFO',
        },
        'dacom': {
            'handlers': ['dacom_file', 'console'],
            'level': 'INFO',
        }
    }
}


from backend.settings_local import *

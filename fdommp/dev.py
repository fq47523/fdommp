"""
Django settings for fdommp project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os,sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r_1*4ephgq7^w1=d6=$lm!e-*65!#li!c^_)6nj7#-fh95t0r@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGIN_URL = '/login/'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dashboard',
    'hosts',
    'api',
    'service',
    'logger',
    'channels',
    'webssh',
    'tasks',
    'assets',
    'databases',

]

CHANNEL_LAYERS = {
    "default": {
       "BACKEND": "channels_redis.core.RedisChannelLayer",  # use redis backend
       "CONFIG": {
            "hosts": [('127.0.0.1', 6379)],
           },
       },
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'logger.PlatformLogHandler.HostLog',
    'logger.PlatformLogHandler.UserLog',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # SessionAuthentication-ajax情况下：csrf中间件要开启，ajax提交的页面需要有{%csrftoken%}，
        # var csrftoken = $.cookie('csrftoken')
        # headers:{'X-CSRFToken':csrftoken}
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3598),
}

ROOT_URLCONF = 'fdommp.urls'


ASGI_APPLICATION = 'fdommp.routing.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils._template_variable.user_var',
            ],
        },
    },
]

WSGI_APPLICATION = 'fdommp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'fdommp',
#         'USER': 'root',
#         'PASSWORD': 'fdommp',
#         'HOST': '192.168.79.134',
#         'PORT': '3306',
#     }
# }




# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# customize
FD_CELERY_BROKER = 'redis://127.0.0.1:6379/5'
FD_CELERY_BACKEND = 'redis://127.0.0.1:6379/6'
FD_REDIS_POOL = {'ip':'127.0.0.1','prot':6379}
FD_ES_IP = '192.168.79.141'
FD_ES_PORT = 9200

FD_ZABBIX_API_URL = 'http://192.168.79.133/api_jsonrpc.php'
FD_ZABBIX_USER = 'admin'
FD_ZABBIX_PASSWD = 'zabbix'


FD_ANSIBLE_HOSTS_FILE = BASE_DIR+'/conf/ansible_hosts'

FD_SERVER_SHELL_SCRIPT = BASE_DIR+'/conf/server.sh'
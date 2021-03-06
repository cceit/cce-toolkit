"""
Django settings for sample_app project.

Generated by 'django-admin startproject' using Django 1.8.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import codecs
import os
from ConfigParser import SafeConfigParser
from os.path import dirname, normpath, join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(BASE_DIR)
STORAGE_DIR = normpath(join(BASE_DIR, 'storage'))

# STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(STORAGE_DIR, 'static'))

# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(STORAGE_DIR, 'media'))

MEDIA_URL = '/media/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'

FIXTURE_DIRS = (
    normpath(join(BASE_DIR, 'fixtures')),
)

# Application definition

DJANGO_APPS = (
    'toolkit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'cuser',  # CurrentUserField
    'widget_tweaks',  # django widget tweaks
    'django_behave',
    'splinter',
)
CUSTOM_APPS = (
    'boards',
    'tasks',
    'profiles',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'cuser.middleware.CuserMiddleware',  # CurrentUserField
)

ROOT_URLCONF = 'daboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(BASE_DIR, 'templates')),
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

WSGI_APPLICATION = 'daboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
CONFIG_PATH = os.path.join(BASE_DIR, "daboard/configs.ini")
config = SafeConfigParser()

LOCAL = 'local'
DEV = 'dev'
UAT = 'uat'
PROD = 'prod'
ENV = LOCAL

IS_LOCAL = ENV == 'local'
IS_DEV = ENV == 'dev'
IS_UAT = ENV == 'uat'
IS_PROD = ENV == 'prod'

try:
    with codecs.open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config.readfp(f)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': config.get('default', 'name'),
                'USER': config.get('default', 'user'),
                'PASSWORD': config.get('default', 'password'),
                'HOST': config.get('default', 'host')
            },
        }
        ENV = config.get('default', 'env')
        SECRET_KEY = config.get('default', 'key')
except IOError:
    pass


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIRS = (normpath(join(BASE_DIR, 'assets')),)
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = "/"

# project_name = 'sample_app'
# FABRIC_SETTINGS = {
#     'PROJECT_NAME': project_name,
#     'GIT_LINK': 'https://github.com/cceit/cce-toolkit.git',
#     'SERVERS': {
#         'uat': {
#             'name': 'latest',
#             'branch': 'latest',
#             'production': False,
#             'server': 'user@server',
#             'project_dir': '/home/project/app',
#             'virtualenv': '/home/project/env',
#             'django_root': '/home/project/app',
#             'settings_file': '/app/dir/settings.py',
#             'settings_param': 'dir.settings',
#             'requirements_path': '/home/project/app/',
#         },
#     }
# }


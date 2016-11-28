import json
import os
from os.path import dirname, normpath, join

BASE_DIR = os.path.abspath(os.path.dirname(__name__))
SITE_ROOT = dirname(BASE_DIR)
STORAGE_ROOT = normpath(join(SITE_ROOT, 'storage'))
STATIC_ROOT = normpath(join(STORAGE_ROOT, 'static'))
MEDIA_ROOT = normpath(join(STORAGE_ROOT, 'media'))
CONFIGS_ROOT = os.path.join(SITE_ROOT, "configs")
CONFIGS_FIXTURE = os.path.join(CONFIGS_ROOT, "configs.json")
STATICFILES_DIRS = (normpath(join(BASE_DIR, 'assets')),)
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = "/"

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'cuser.middleware.CuserMiddleware',  # CurrentUserField
]

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
                'django_settings_export.settings_export',
                'toolkit.context_processors.export_site_object',
                'toolkit.apps.breadcrumbs.middleware.context.process_context',
            ],
        },
    },
]

FIXTURE_DIRS = (
    normpath(join(BASE_DIR, 'fixtures')),
)

DJANGO_APPS = [
    'toolkit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'cuser',
    'widget_tweaks',
    'django_behave',
    'splinter',
    'hijack',
    'hijack_admin',
    'compat',
]

TOOLKIT_APPS = [
    'toolkit.apps.breadcrumbs',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + TOOLKIT_APPS

LOCAL = 'local'
DEV = 'dev'
UAT = 'uat'
PROD = 'prod'
ENV = LOCAL
app_config = {}

try:
    with open(CONFIGS_FIXTURE) as data_file:
        app_config = json.load(data_file)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': app_config['database']['name'],
                'USER': app_config['database']['username'],
                'PASSWORD': app_config['database']['password'],
                'HOST': app_config['database']['host']
            },
        }
        ENV = app_config['ENV']
        SECRET_KEY = app_config['SECRET_KEY']
        ALLOWED_HOSTS = []

        DEFAULT_FROM_EMAIL = app_config['DEFAULT_FROM_EMAIL']
        EMAIL_HOST = app_config['EMAIL_HOST']
        IS_OU = app_config['application']['IS_OU']

except IOError:
    pass

IS_LOCAL = ENV == 'local'
IS_DEV = ENV == 'dev'
IS_UAT = ENV == 'uat'
IS_PROD = ENV == 'prod'
DEBUG = not IS_PROD

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATEPICKER_FORMAT = '%m/%d/%Y'
AUTH_USER_MODEL = 'auth.User'

BOOLEAN_CHOICES = (
    (True, "Yes"),
    (False, "No"),
)


SITE_ID = 1
WSGI_APPLICATION = 'nucleus.wsgi.application'
ROOT_URLCONF = 'nucleus.urls'

TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8000-8100'

UNUSABLE_PASSWORD = "!"

HIJACK_LOGIN_REDIRECT_URL = '/'
HIJACK_LOGOUT_REDIRECT_URL = '/admin/auth/user/'
HIJACK_ALLOW_GET_REQUESTS = True


SETTINGS_EXPORT = [
    'ENV',
    'IS_LOCAL',
    'IS_DEV',
    'IS_UAT',
    'IS_PROD',
    'IS_OU',
    'DEFAULT_FROM_EMAIL',
]
SECRET_KEY = 'ctqay9sxnh2$mvaii)-^r@^dw#kj%4jsb9!lqn*k1vuid_*dcc'

INSTALLED_APPS = (
    'cuser',
    'toolkit',

    'django.contrib.auth',
    'django.contrib.contenttypes'
)

MIDDLEWARE_CLASSES = (
    'cuser.middleware.CuserMiddleware',
)

FABRIC_SETTINGS = {
    'GIT_LINK': 'https://github.com/cceit/cce-toolkit.git',
    'PROJECT_NAME': 'Toolkit Docs',
    'SERVERS': {

    }
}

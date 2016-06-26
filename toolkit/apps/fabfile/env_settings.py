from django.conf import settings
from fabric.state import env

PRIVATE_DIR = getattr(settings, "FABRIC_SETTINGS")
project_name = settings.FABRIC_SETTINGS['PROJECT_NAME']
git_link = settings.FABRIC_SETTINGS['GIT_LINK']
env.roledefs = settings.FABRIC_SETTINGS['SERVERS']

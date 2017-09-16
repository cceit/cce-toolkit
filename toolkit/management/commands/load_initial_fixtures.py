from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    loads list of initial fixtures
    Usage: python manage.py load_initial_fixtures --env [local|uat|dev|prod]

    Add the following dictionary to the django settings file


    INITIAL_FIXTURES = {
        'common': [''],
        'uat': [''],
        'dev': [''],
        'prod': [''],
        'local': [''],
    }
    """
    help = 'loads list of initial fixtures'

    option_list = BaseCommand.option_list + (
        make_option('--env',
                    action='store',
                    dest='env',
                    default=False,
                    help='sets environment'),
    )

    def handle(self, *args, **options):
        try:
            initial_fixtures = settings.INITIAL_FIXTURES['common'] + \
                               settings.INITIAL_FIXTURES[options['env'] if options['env'] else settings.ENV]
        except NameError:
            raise NotImplementedError('Did not find the environmental variable. Specify variable in settings.ENV or '
                                      'provide a parameter')
        for fixture in initial_fixtures:
            call_command('loaddata', fixture)

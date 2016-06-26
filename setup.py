from setuptools import setup

setup(
    name="cce_toolkit",
    version="1.0.0-beta",
    author_email='devs@cce.ou.edu',
    description=('A collection of python helpers and custom Django views, '
                 'forms and models created for rapid development of Management'
                 ' Information Systems'),
    author='University of Oklahoma - College of Continuing Education - IT',
    license='BSD',

    extras_require={
        "cuser": ["django-cuser"],
    },
    classifiers=[
        'Development Status :: 1.0.0-beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    url='https://github.com/cceit/cce-toolkit.git',
    packages=['toolkit'],
    include_package_data=True,
    package_data={
        'toolkit': [
            '*.py',
            'mixins/*.py',
            'fabfile/*.py',
            'breadcrumbs/*.py',
            'breadcrumbs/middleware/*.py',
            'breadcrumbs/templates/*.html',
            'breadcrumbs/templatetags/*.py',
            'templatetags/*.py',
            'templates/*.html',
            'templates/comments/*.html',
            'templates/form_fragments/*.html',
            'templates/registration/*.html',
            'static/toolkit/*.js',
            'static/toolkit/*.css',
            'static/*.js',
            'static/*.css',
            'bdd/*.py',
            'migrations/*.py',
        ],
    },
    zip_safe=False,
)

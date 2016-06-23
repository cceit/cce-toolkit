from setuptools import setup

setup(
    # Metadata for PyPI; nice to have but not required
    name="cce_toolkit",
    version="1.4.7",
    description='A collection of tools used to speed up the development of management information systems using Django',
    author='CCE Devs',
    license='BSD-3',
    # I don't think this url is required either, but it's nice to have
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
    zip_safe=False,  # important, forces it to install as directories and not .zip
)

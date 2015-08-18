from setuptools import setup
setup(
    name="cce_toolkit",
    version="0.1",
    url='ssh://code.ce.ou.edu/var/git/cce_toolkit',
    packages=['toolkit'],
    package_dir={'toolkit': 'toolkit'},  # this shouldn't be necessary
    include_package_data=True,
    package_data={'toolkit': ['*.py','mixins/*.py','templatetags/*.py','test_tools/*.py','test_tools/steps/*.py']},
    description='A collection of tools for use in CCE-IT projects',
    author='CCE Devs',
    license='All Rights Reserved',
    zip_safe=False,
)


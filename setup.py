from setuptools import setup
setup(
    # Metadata for PyPI; nice to have but not required
    name="cce_toolkit",
    version="0.1",
    description='A collection of tools for use in CCE-IT projects',
    author='CCE Devs',
    license='All Rights Reserved',
    # I don't think this url is required either, but it's nice to have
    url='ssh://code.ce.ou.edu/var/git/cce_toolkit',
    packages=['toolkit'],
    zip_safe=False,  # important, forces it to install as directories and not .zip
)


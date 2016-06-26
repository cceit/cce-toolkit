from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


def auto_admin_register(app_name, exclude=()):
    """Helper allows you to register models to django-admin in bulk.

    Register all unregistered models in the given app with the admin site.
    Any previously-registered models will retain their original registration.


    :param string  app_name: the name of the app to auto_admin_register.
    :param iterable exclude: an iterable of model names to exclude from
        registration


    Usage:
        .. code-block:: python
            :linenos:

            from polls.models import Poll
            from toolkit.admin import auto_admin_register

            auto_admin_register(__package__, exclude=(Poll.__name__, ))

    Recommended usage:
        make **auto_admin_register(__package__)** the last line in desired
        admin.py files.

    .. caution:: Registers all models found in **app_name** that are not listed
        in **exclude** with the django-admin site.

    Author:
        Fredrick Wagner

    """

    from django.apps import apps

    app = apps.get_app_config(app_name)
    for k, model in app.models.items():
        if model.__name__ not in exclude:
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass

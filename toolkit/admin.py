from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

def auto_admin_register(app_name, exclude=()):
    """Register all remaining models in the given app with the admin site.

    Any previously-registered models will retain their original registration.

    Recommended usage: make `auto_admin_register(__package__)` the last line in
    desired admin.py files.

    Args:
        app_name: the name of the app to auto_admin_register.
        exclude: an iterable of model names to not register.
    Side effects:
        Registers all models found in app_name that are not listed in exclude
        with the admin site.

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

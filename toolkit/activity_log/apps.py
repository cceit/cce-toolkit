from django.apps import AppConfig


class ActivityLogConfig(AppConfig):
    name = "activity_log"
    verbose_name = "Activity Log"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals

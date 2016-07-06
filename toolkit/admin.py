from django.contrib import admin
from toolkit.apps.activity_log.models import ActivityLog, ActivityType

admin.site.register(ActivityType)
admin.site.register(ActivityLog)

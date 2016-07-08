from django.contrib import admin
from toolkit.apps.toolkit_activity_log.models import ToolkitActivityLog, ToolkitActivityType

admin.site.register(ToolkitActivityType)
admin.site.register(ToolkitActivityLog)

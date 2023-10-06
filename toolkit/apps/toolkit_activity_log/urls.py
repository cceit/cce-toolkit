from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import ToolkitActivityLogListView

urlpatterns = [
    path(r'^browse/$', login_required(ToolkitActivityLogListView.as_view()), name='browse_activity_logs', ),
]

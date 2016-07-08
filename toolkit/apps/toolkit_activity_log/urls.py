from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ToolkitActivityLogListView

urlpatterns = [
    url(r'^browse/$', login_required(ToolkitActivityLogListView.as_view()), name='browse_activity_logs', ),
]

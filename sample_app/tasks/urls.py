from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from tasks.views import TaskCreateView, TaskUpdateView, TaskDeleteView, \
    TaskDetailView, TaskListView, TaskStatusUpdateView, CompletedTaskListView

urlpatterns = [
        url(r'^(?P<pk>\d+)/', include([
            url(r'^edit/$', login_required(TaskUpdateView.as_view()),
                name='edit_task'),
            url(r'^update_status/$',
                login_required(TaskStatusUpdateView.as_view()),
                name='update_task_status'),
            url(r'^delete/$', login_required(TaskDeleteView.as_view()),
                name='delete_task'),
            url(r'^$', login_required(TaskDetailView.as_view()),
                name='view_task'),
        ])),
        url(r'^add/', login_required(TaskCreateView.as_view()),
            name='add_task'),
        url(r'^completed/', login_required(CompletedTaskListView.as_view()),
            name='browse_completed_tasks'),
        url(r'^$', login_required(TaskListView.as_view())
            , name='browse_tasks'),
]

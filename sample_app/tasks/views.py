from django.core.urlresolvers import reverse
from toolkit.views import CCECreateView, CCEDeleteView, \
    CCEUpdateView, ReportDownloadSearchView, CCEDetailView

from tasks.forms import TaskSimpleSearch, TaskAdvancedSearchForm, TaskForm, \
    UpdateTaskStatusForm, CompletedTaskAdvancedSearchForm
from tasks.models import Task


class TaskListView(ReportDownloadSearchView):
    model = Task
    page_title = "Browse Tasks"
    search_form_class = TaskSimpleSearch
    advanced_search_form_class = TaskAdvancedSearchForm
    sidebar_group = ['tasks', 'browse_tasks']
    columns = [
        ('Title', 'title'),
        ('Description', 'description'),
        ('Board', 'board.name'),
        ('Status', lambda x: x.get_status_display(), '2', 'status'),
        ('Created at', 'created_at'),
        ('Created by', 'created_by'),
    ]
    paginate_by = 2
    show_context_menu = True

    def get_reports(self):
        return {
            'basic_report': {'name': 'Quick Task Reports',
                             'method': 'task_report'},
            'details_report': {'name': 'Detailed Task Reports',
                               'method': 'detailed_task_report'},
        }


class CompletedTaskListView(TaskListView):
    page_title = "Browse Completed Tasks"
    sidebar_group = ['tasks', 'browse_completed_tasks']
    advanced_search_form_class = CompletedTaskAdvancedSearchForm

    def get_queryset(self):
        return super(CompletedTaskListView, self).get_queryset()\
            .filter(status=Task.COMPLETE)


class TaskCreateView(CCECreateView):
    model = Task
    sidebar_group = ['tasks']
    page_title = 'Create Task'
    form_class = TaskForm
    success_message = "Task Created Successfully"


class TaskUpdateView(CCEUpdateView):
    model = Task
    page_title = 'Edit Status'
    sidebar_group = ['tasks']
    form_class = TaskForm
    success_message = "Task Edited Successfully"
    show_context_menu = True


class TaskStatusUpdateView(CCEUpdateView):
    model = Task
    page_title = 'Update Task Status'
    sidebar_group = ['tasks']
    form_class = UpdateTaskStatusForm
    success_message = "Task Status updated Successfully"
    show_context_menu = True


class TaskDeleteView(CCEDeleteView):
    model = Task
    sidebar_group = ['tasks']
    page_title = "Delete Task"
    success_message = "Task Deleted Successfully"
    show_context_menu = True

    def get_success_url(self):
        return reverse('browse_tasks')


class TaskDetailView(CCEDetailView):
    model = Task
    page_title = "Task Details"
    sidebar_group = ['tasks']
    detail_fields = [
        ('Title', 'title'),
        ('Description', 'description'),
        ('Created By', 'created_by'),
        ('Image', 'image'),
        ('Attachment', 'attachment'),
        ('Status', lambda x: x.get_status_display()),
        ('Completed at', 'completed_at'),
        ('Board', 'board.name'),
        ('Created At', 'created_at'),
        ('Last Updated By', 'last_updated_by'),
        ('Last Updated At', 'last_updated_at'),
    ]
    show_context_menu = True

    def context_menu_items(self):
        items = super(TaskDetailView, self).context_menu_items()
        items.append(
            (
                "Update Status",
                reverse('update_task_status',
                        kwargs={'pk': self.kwargs['pk']}),
                "glyphicon glyphicon-edit",
            )
        )
        return items

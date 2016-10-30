from django import forms
from django.contrib.auth.models import User
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, CCEModelForm

from boards.models import Board
from tasks.models import Task


class TaskSimpleSearch(CCESimpleSearchForm):
    search_placeholder = 'Search Tasks'

    class Meta(CCESimpleSearchForm.Meta):
        model = Task
        field_lookups = {'search': ('title__icontains',
                                    'description__icontains',
                                    )}


class TaskAdvancedSearchForm(CCEModelSearchForm):
    """Advanced Search Form for Tasks"""
    description = forms.CharField(max_length=1000, required=False)
    created_at = forms.DateField(required=False)
    created_by = forms.ModelChoiceField(User.objects.all(), required=False)
    boards = forms.ModelMultipleChoiceField(Board.objects.all(),
                                            required=False)

    class Meta:
        model = Task
        field_lookups = {
            'title': 'title__icontains',
            'description': 'description__icontains',
            'boards': 'board__pk__in',
            'status': 'status',
            'created_at': 'created_at__startswith',
            'created_by': 'created_by',
        }

        fields = (
            'title',
            'description',
            'boards',
            'status',
            'created_at',
            'created_by'
        )


class CompletedTaskAdvancedSearchForm(TaskAdvancedSearchForm):
    """Advanced Search Form for Completed Tasks"""

    class Meta:
        model = Task
        field_lookups = {
            'title': 'title__icontains',
            'description': 'description__icontains',
            'boards': 'board__pk__in',
            'created_at': 'created_at__startswith',
            'created_by': 'created_by',
        }

        fields = (
            'title',
            'description',
            'boards',
            'created_at',
            'created_by'
        )


class TaskForm(CCEModelForm):
    class Meta:
        model = Task
        fields = ('title',
                  'description',
                  'attachment',
                  'image',
                  'board', )
        help_texts = {
            'title': 'asddsadsa asd asd asdasd asd asd asd asdasd asd asd asd asd asasdsadas as ads asasd sad'
        }


class UpdateTaskStatusForm(CCEModelForm):
    class Meta:
        model = Task
        fields = ('status',
                  'completed_at', )

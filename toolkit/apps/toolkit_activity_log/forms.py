from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.forms import ModelChoiceField
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm

from .models import ToolkitActivityLog


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s (%s)" % (obj.first_name, obj.last_name, obj.username)


class ActivityLogSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search by Type, Activity, or Description'

    class Meta(CCESimpleSearchForm.Meta):
        model = ToolkitActivityLog
        field_lookups = {
            'search': (
                'activity_type__icontains',
                'summary__icontains',
                'description__icontains',
            )
        }


class ActivityLogAdvancedSearchForm(CCEModelSearchForm):
    activity = forms.CharField(required=False)
    description = forms.CharField(required=False)
    user = UserModelChoiceField(queryset=get_user_model().objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = ToolkitActivityLog
        field_lookups = {
            'activity_type': 'activity_type',
            'activity': 'summary__icontains',
            'description': 'description__icontains',
            'user': 'created_by',
            'group': 'activity_type__groups'
        }
        fields = (
            'activity_type',
            'activity',
            'description',
            'user',
            'group',
        )

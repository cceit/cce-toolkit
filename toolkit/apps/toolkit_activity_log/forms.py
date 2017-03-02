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
    search_placeholder = 'Search by Type/Activity/Description/IP'

    class Meta(CCESimpleSearchForm.Meta):
        model = ToolkitActivityLog
        field_lookups = {
            'search': (
                'activity_type__icontains',
                'summary__icontains',
                'description__icontains',
                'ip_address_icontains',
            )
        }


class ActivityLogAdvancedSearchForm(CCEModelSearchForm):
    activity = forms.CharField(required=False)
    description = forms.CharField(required=False)
    user = UserModelChoiceField(queryset=get_user_model().objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    date_start = forms.DateField(required=False)
    date_end = forms.DateField(required=False)

    class Meta:
        model = ToolkitActivityLog
        field_lookups = {
            'activity_type': 'activity_type',
            'activity': 'summary__icontains',
            'description': 'description__icontains',
            'ip_address': 'ip_address__icontains',
            'user_agent': 'user_agent__icontains',
            'user': 'created_by',
            'group': 'activity_type__groups',
            'date_start': 'created_at__gte',
            'date_end': 'created_at__lte',
        }
        fields = (
            'activity_type',
            'activity',
            'description',
            'ip_address',
            'user_agent',
            'user',
            'group',
            'date_start',
            'date_end',
        )

        labels = {
            'activity_type': 'Activity Type',
            'ip_address': 'IP Address',
            'user_agent': 'User Agent',
        }

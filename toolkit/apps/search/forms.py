from django import forms
from toolkit.forms import CCEModelForm
from .models import SearchFilter


class SearchFilterForm(CCEModelForm):
    class Meta:
        model = SearchFilter
        fields = ('name', 'user', 'visibility', 'query_string', 'view')
        widgets = {
            'user': forms.HiddenInput,
            'query_string': forms.HiddenInput,
            'view': forms.HiddenInput,
        }

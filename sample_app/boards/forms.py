from django import forms
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, CCEModelForm

from boards.models import Board


class BoardSimpleSearch(CCESimpleSearchForm):
    search_placeholder = 'Search Boards'

    class Meta(CCESimpleSearchForm.Meta):
        model = Board
        field_lookups = {'search': ('name__icontains', 'description__icontains')}


class BoardAdvancedSearchForm(CCEModelSearchForm):
    """Advanced Search Form for Events"""
    description = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = Board
        field_lookups = {
            'name': 'name__icontains',
            'description': 'description__icontains',
        }

        fields = (
            'name',
            'description',
        )


class BoardForm(CCEModelForm):
    class Meta:
        model = Board
        fields = ('image',
                  'name',
                  'description',)

from django import forms
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, CCEModelForm

from boards.models import Board
from planks.models import Plank


class PlankSimpleSearch(CCESimpleSearchForm):
    search_placeholder = 'Search Planks'

    class Meta(CCESimpleSearchForm.Meta):
        model = Plank
        field_lookups = {'search': 'title__icontains'}


class PlankAdvancedSearchForm(CCEModelSearchForm):
    """Advanced Search Form for Events"""
    description = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = Plank
        field_lookups = {
            'title': 'title__icontains',
        }

        fields = (
            'title',
        )


class PlankForm(CCEModelForm):
    class Meta:
        model = Plank
        fields = ('image',
                  'title',
                  'board',
                  'owner',
        )
        widgets = {'board': forms.HiddenInput,
                   'owner': forms.HiddenInput}

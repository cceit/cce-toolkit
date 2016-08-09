from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, forms, CCEModelForm

from splinters.models import Splinter


class SplinterSimpleSearch(CCESimpleSearchForm):
    search_placeholder = 'Search Planks'

    class Meta(CCESimpleSearchForm.Meta):
        model = Splinter
        field_lookups = {'search': 'owner__icontains'}


class SplinterAdvancedSearchForm(CCEModelSearchForm):
    """Advanced Search Form for Events"""

    class Meta:
        model = Splinter
        field_lookups = {
            'owner': 'owner__username__icontains',
            'comment': 'comment__icontains',
        }

        fields = (
            'owner',
            'comment',
        )


class SplinterForm(CCEModelForm):
    class Meta:
        model = Splinter
        fields = (
            'plank',
            'owner',
            'comment',
        )
        widgets = {'owner': forms.HiddenInput,
                   'plank': forms.HiddenInput}

from django import forms
from django.conf import settings
from django.forms import NullBooleanSelect

from .mixins.forms import SearchFormMixin


class SearchForm(SearchFormMixin, forms.Form):
    pass


class CCEModelSearchForm(SearchFormMixin, forms.ModelForm):
    required_fields = []
    def __init__(self, *args, **kwargs):
        """
        Disables the require property of all form fields, allowing them to be
        used as optional search fields.
        """
        super(CCEModelSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in self.required_fields:
                self.fields[field].required = False


class CCESimpleSearchForm(CCEModelSearchForm):
    """SearchForm used to search for CESL Session

    :fields:
            - search

    """
    search = forms.CharField(max_length=200, required=False)
    search_placeholder = ''

    class Meta:
        fields = ('search',)

    def __init__(self, *args, **kwargs):
        """
        Disables the require property of all form fields, allowing them to be
        used as optional search fields.
        """
        super(CCESimpleSearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget = forms.TextInput(attrs={'placeholder': self.search_placeholder})


class DynamicNullBooleanSelect(NullBooleanSelect):
    """
    An overriden Select widget to be used with NullBooleanField.
    Takes a kwarg "null_label" that indicates the text on the null option.
    """
    def __init__(self, attrs=None, null_label=None, true_label=None, false_label=None):
        if null_label is None:
            null_label = 'Unknown'
        if true_label is None:
            true_label = 'True'
        if false_label is None:
            false_label = 'False'
        choices = (
            ('1', null_label),
            ('2', true_label),
            ('3', false_label)
        )
        super(NullBooleanSelect, self).__init__(attrs, choices)


class ReportSelector(forms.Form):
    def __init__(self, user, *args, **kwargs):
        reports_list = kwargs.pop('reports_list')
        super(ReportSelector, self).__init__(*args, **kwargs)
        self.fields['get_reports'] = forms.ChoiceField(choices=[('', 'Select Report')] +
                                                               [(k, v['name']) for k, v in reports_list.items()])


def cce_formfield_callback(f, **kwargs):
    formfield = f.formfield(**kwargs)
    if isinstance(formfield, forms.DateField):
        formfield.widget.format = settings.DATEFIELD_FORMAT
    return formfield


class CCEModelFormMetaclass(forms.models.ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        if 'formfield_callback' not in attrs:
            attrs['formfield_callback'] = cce_formfield_callback
        return super(CCEModelFormMetaclass, mcs).__new__(mcs, name, bases, attrs)


class CCEModelForm(forms.ModelForm):
    __metaclass__ = CCEModelFormMetaclass

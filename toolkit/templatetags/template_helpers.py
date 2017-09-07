import os
from django import template
from django.forms import widgets

from toolkit.forms import DynamicNullBooleanSelect
from toolkit.helpers.utils import snakify

register = template.Library()


@register.filter
def is_date_field(formfield):
    """
    Template tag used in a django template to check if a form field is a 
     date field
     
    :param FormField formfield: Django form field
    :returns bool: True if FormField is a date field
    """
    styled_widgets = [widgets.DateInput,
                      ]
    return type(formfield.field.widget) in styled_widgets


@register.filter
def is_datetime_field(formfield):
    """
    Template tag used in a django template to check if a form field is a 
     datetime field
     
    :param FormField formfield: Django form field
    :returns bool: True if FormField is a datetime field
    """
    styled_widgets = [widgets.DateTimeInput,
                      ]
    return type(formfield.field.widget) in styled_widgets


@register.filter
def is_time_field(formfield):
    """
    Template tag used in a django template to check if a form field is a 
     time field
     
    :param FormField formfield: Django form field
    :returns bool: True if FormField is a time field
    """
    styled_widgets = [widgets.TimeInput,
                      ]
    return type(formfield.field.widget) in styled_widgets


@register.filter
def is_bootstrap_styled_field(formfield):
    """
    Template tag used in a django template to check if a form field can be
     styled using bootstrap
     
    :param FormField formfield: Django form field
    :returns bool: True if the widget of the form field is one of the following
        - widgets.TextInput
        - widgets.Textarea
        - widgets.NumberInput
        - widgets.EmailInput
        - widgets.Select
        - widgets.DateInput
        - widgets.PasswordInput
        - DynamicNullBooleanSelect
        - widgets.URLInput
        - widgets.NullBooleanSelect
        - widgets.SelectMultiple
    
    """
    styled_widgets = [
        widgets.TextInput,
        widgets.Textarea,
        widgets.NumberInput,
        widgets.EmailInput,
        widgets.Select,
        widgets.DateInput,
        widgets.PasswordInput,
        DynamicNullBooleanSelect,
        widgets.URLInput,
        widgets.NullBooleanSelect,
        widgets.SelectMultiple,
    ]
    return type(formfield.field.widget) in styled_widgets


@register.tag
def make_list(parser, token):
    """
    Template tag to create a python list within a Django template

    Usage:
        .. code-block:: python
            :linenos:

            {% make_list var1 var2 var3 as some_list %}

    http://stackoverflow.com/questions/3715550/creating-a-list-on-the-fly-in-a-django-template
    """
    bits = list(token.split_contents())
    if len(bits) >= 4 and bits[-2] == "as":
        varname = bits[-1]
        items = bits[1:-2]
        return MakeListNode(items, varname)
    else:
        raise template.TemplateSyntaxError(
            "%r expected format is 'item [item ...] as varname'" % bits[0])


@register.filter
def snake(value):
    return snakify(value)


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


class MakeListNode(template.Node):
    """
    Helper method for make_list

    http://stackoverflow.com/questions/3715550/creating-a-list-on-the-fly-in-a-django-template
    """

    def __init__(self, items, varname):
        self.items = map(template.Variable, items)
        self.varname = varname

    def render(self, context):
        context[self.varname] = [i.resolve(context) for i in self.items]
        return ""

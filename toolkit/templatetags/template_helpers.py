from django import template
from django.forms import widgets

from toolkit.forms import DynamicNullBooleanSelect

register = template.Library()


@register.filter
def is_date_field(value):
    styled_widgets = [widgets.DateInput,
                      ]
    return type(value.field.widget) in styled_widgets


@register.filter
def is_datetime_field(value):
    styled_widgets = [widgets.DateTimeInput,
                      ]
    return type(value.field.widget) in styled_widgets


@register.filter
def is_time_field(value):
    styled_widgets = [widgets.TimeInput,
                      ]
    return type(value.field.widget) in styled_widgets


@register.filter
def is_bootstrap_styled_field(value):
    styled_widgets = [widgets.TextInput,
                      widgets.Textarea,
                      widgets.NumberInput,
                      widgets.EmailInput,
                      widgets.Select,
                      widgets.DateInput,
                      DynamicNullBooleanSelect,
                      ]
    return type(value.field.widget) in styled_widgets


@register.tag
def make_list(parser, token):
    """
    http://stackoverflow.com/questions/3715550/creating-a-list-on-the-fly-in-a-django-template
    """
    bits = list(token.split_contents())
    if len(bits) >= 4 and bits[-2] == "as":
        varname = bits[-1]
        items = bits[1:-2]
        return MakeListNode(items, varname)
    else:
        raise template.TemplateSyntaxError("%r expected format is 'item [item ...] as varname'" % bits[0])


class MakeListNode(template.Node):
    """
    http://stackoverflow.com/questions/3715550/creating-a-list-on-the-fly-in-a-django-template
    """

    def __init__(self, items, varname):
        self.items = map(template.Variable, items)
        self.varname = varname

    def render(self, context):
        context[self.varname] = [i.resolve(context) for i in self.items]
        return ""

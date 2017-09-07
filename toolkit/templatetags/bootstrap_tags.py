import datetime
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import Manager
from django.db.models.fields.files import FieldFile, ImageFieldFile
import arrow
register = template.Library()


@register.filter
def boolean_icon(value):
    """
    :param Bool value: Nullable boolean value
    :returns html: i tag with fontawesome icon representation
    """
    if value:
        return mark_safe('<i class="true_icon fa fa-check" aria-hidden="true"></i>')
    elif value is None:
        return '--'
    else:
        return mark_safe('<i class="false_icon fa fa-times" aria-hidden="true"></i>')


def follow_path(ob, dotted_attrs):
    new_ob = ob
    attrs = dotted_attrs.split('.')
    for attr in attrs:
        if hasattr(new_ob, attr):
            new_ob = getattr(new_ob, attr)
            if callable(new_ob) and not isinstance(new_ob, Manager):
                new_ob = new_ob()
        else:
            raise Exception("Bad dotted attributes passed to %s: %s"
                            % (type(new_ob), dotted_attrs))
    return new_ob


@register.filter
def render_detail(value, param):
    """
    :returns: appropriate html rendering of value
    """
    if value is None:
        return "--"
    if isinstance(value, bool):
        return boolean_icon(value)
    if isinstance(value, datetime.datetime):
        arrow_obj = arrow.get(value)
        return arrow_obj.format("MM/D/YYYY, h:mm a")
    elif isinstance(value, datetime.date):
        arrow_obj = arrow.get(value)
        return arrow_obj.format("MM/D/YYYY")
    elif isinstance(value, datetime.time):
        return value.strftime("%I:%M %p").lstrip('0')
    elif isinstance(value, Manager):
        # param is an optional dotted path to follow on each related object
        related_objs = list(value.all())
        if param:
            swap = related_objs
            related_objs = [follow_path(o, param) for o in swap]
        return ', '.join([str(thing) for thing in related_objs])
    elif isinstance(value, ImageFieldFile):
        if not value:
            return '--'
        return mark_safe('<img src="%s%s" width="200px" height="200px">' %
                         (settings.MEDIA_URL, value))
    elif isinstance(value, FieldFile):
        if not value:
            return '--'
        return mark_safe('<a href="%s">Download</a>' % value.url)
    return value

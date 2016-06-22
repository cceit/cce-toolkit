import re

import unicodedata

from django.db.models.fields.related import RelatedField
from django.shortcuts import _get_queryset
from django.utils import six
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.functional import allow_lazy
from django.utils.safestring import mark_safe, SafeText


def usernamify(s):
    """Remove characters invalid for use in a username and convert to lowercase.

    If s contains no valid characters, the returned value will be the empty
    string, which is not a valid username on its own.

    Author: Fredrick Wagner
    """
    special_chars = '@.+-_'
    return ''.join(c for c in s if c.isalnum() or c in special_chars).lower()


def generate_username_from_name(first_name, last_name):
    """Return a unique, valid username based off the given first and last names.

    Raises IndexError if first_name is empty or contains no characters valid for
    use in a username.
    """
    base_username = 'user'
    if first_name:
        base_username = usernamify(first_name)[0]
    if last_name:
        base_username += usernamify(last_name)

    username = base_username
    # If the username is taken, add a serial number.
    number = 1
    while User.objects.filter(username=username).exists():
        username = base_username + str(number)
        number += 1
    return username


def replace_key(old_key, new_key, dictionary):
    if old_key in dictionary:
        value = dictionary.pop(old_key)
        dictionary[new_key] = value
    return dictionary


def snakify(value):
    """
    Converts to ASCII. Converts spaces to underscores. Removes characters that
    aren't alphanumerics, underscores, or hyphens. Converts to lowercase.
    Also strips leading and trailing whitespace.
    """
    value = force_text(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return mark_safe(re.sub('[-\s]+', '_', value))
snakify = allow_lazy(snakify, six.text_type, SafeText)


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def _hasfield(model_fields, field_name):
    """
    Check if field name exists in list of model fields

    Args:
        model_fields: List of Django Model object fields
        field_name: attribute string, dotted or dunderscored. example: 'user.first_name' or 'user__first_name'

    Returns: Field object or False

    """
    for field in model_fields:
        if field.name == field_name:
            return field
    return False


def hasfield(model, field_name):
    """
    Returns whether the attribute string is a valid field on the model or its related models

    Args:
        model: Django Model object
        field_name: attribute string, dotted or dunderscored. example: 'user.first_name' or 'user__first_name'

    Returns: Field object or False

    """
    field_name = field_name.replace('__', '.')
    model_fields = model._meta.fields
    field_names = field_name.split('.')
    fields_count = len(field_names)
    i = 0
    for field_name in field_names:
        related_field = _hasfield(model_fields, field_name)
        # if no match found or if a match found and this is the last field to lookup, return the result
        if not related_field or (related_field and i == (fields_count - 1)):
            return related_field

        # if its a ForeignKey or a ManytoManyField or a OnetoOneField, look through the related model
        if isinstance(related_field, RelatedField):
            model_fields = related_field.related_model._meta.fields
        i += 1
    return False

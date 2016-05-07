import re

import unicodedata

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

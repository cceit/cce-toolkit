from django.db import models
from toolkit.mixins.models import ModelPermissionsMixin


class CCEModel(ModelPermissionsMixin, models.Model):
    """
    Abstract base model with permissions mixin.
    """
    class Meta:
        abstract = True


class CCEAuditModel(CCEModel):
    """
    Abstract model with fields for the user and timestamp of a row's creation
    and last update.

    .. note:: - Inherits from **CCEModel**
              - Requires **django-cuser** package to determine current user

    :tags:
        django-cuser
    """
    from cuser.fields import CurrentUserField

    last_updated_by = CurrentUserField(
        related_name='%(app_label)s_%(class)s_last_updated')
    last_updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(add_only=True,
                                  related_name='%(app_label)s_%(class)s_'
                                               'last_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

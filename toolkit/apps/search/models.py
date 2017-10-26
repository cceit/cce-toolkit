from django.db import models
from django.contrib.auth.models import User

from toolkit.models import CCEAuditModel


class SearchFilter(CCEAuditModel):
    PRIVATE = 'private'
    PUBLIC = 'public'
    VISIBILITY_CHOICES = (
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    )

    name = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    visibility = models.CharField(max_length=16, choices=VISIBILITY_CHOICES)
    query_string = models.TextField()
    view = models.CharField(max_length=256)

    class Meta:
        db_table = 'search_filters'
        ordering = ("-created_at", )

    def __unicode__(self):
        return self.name

    @classmethod
    def can_create(cls, user_obj):
        return True

    @classmethod
    def can_view_list(cls, user_obj):
        return True

    def can_update(self, user_obj):
        return True

    def can_view(self, user_obj):
        return True

    def can_delete(self, user_obj):
        return True

from django.urls import reverse
from django.db import models
from toolkit.models import CCEAuditModel


class Board(CCEAuditModel):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __str__(self):
        return u'/b/%s' % self.name

    def get_absolute_url(self):
        return reverse('browse_tasks') + '?boards=%s' % self.pk

    def can_update(self, user_obj):
        return True

    def can_delete(self, user_obj):
        return user_obj.is_staff or self.created_by == user_obj

    def can_create(self, user_obj):
        return True

    def can_view_list(self, user_obj):
        return True

    def can_view(self, user_obj):
        return True

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from toolkit.models import CCEAuditModel


class Profile(CCEAuditModel):
    user = models.ForeignKey(User)
    picture = models.FileField(null=True, blank=True)

    def can_update(self, user_obj):
        return True

    def can_delete(self, user_obj):
        return True

    def can_create(self, user_obj):
        return True

    def can_view_list(self, user_obj):
        return True

    def can_view(self, user_obj):
        return True

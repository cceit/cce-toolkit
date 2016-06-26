from django.db import models
from django.db.models import Q


class ActivityTypePermissionManager(models.Manager):
    def scoped_by_user(self, user_obj):
        return self.filter(Q(groups__user=user_obj) | Q(include_creator=True, activitylog__created_by=user_obj))

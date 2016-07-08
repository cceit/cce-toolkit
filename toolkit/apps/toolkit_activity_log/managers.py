from django.db import models
from django.db.models import Q


class ActivityTypePermissionManager(models.Manager):
    def scoped_by_user(self, user_obj):
        return self.filter(Q(groups__user=user_obj) | Q(include_creator=True))


class ActivitiesPermissionManager(models.Manager):
    def scoped_by_user(self, user_obj):
        return self.filter(Q(activity_type__groups__user=user_obj) | Q(activity_type__include_creator=True,
                                                                       created_by=user_obj))

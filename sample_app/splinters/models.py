from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from toolkit.models import CCEAuditModel

from planks.models import Plank
from splinters.reports import SplinterReports


class Splinter(CCEAuditModel):
    owner = models.ForeignKey(User)
    plank = models.ForeignKey(Plank)
    comment = models.TextField(max_length=1000, unique=False)
    reports = SplinterReports()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.comment)
        self.comment = mark_safe(self.comment.replace("\n", "<br/>"))
        return super(Splinter, self).save(*args, **kwargs)

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

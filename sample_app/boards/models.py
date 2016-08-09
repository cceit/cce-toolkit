from django.db import models
from django.utils.text import slugify
from toolkit.models import CCEAuditModel

from boards.reports import BoardsReports


class Board(CCEAuditModel):
    image = models.FileField(upload_to='board_images', blank=False, null=False)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    created = models.DateTimeField(verbose_name=None, auto_now_add=True, null=True)
    reports = BoardsReports()

    def __unicode__(self):
        return  self.name

    @staticmethod
    def is_admin(userobj):
        return userobj.is_superuser or userobj.is_staff

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Board, self).save(*args, **kwargs)

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

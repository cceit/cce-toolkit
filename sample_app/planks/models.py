from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from toolkit.models import CCEAuditModel

from boards.models import Board


class Plank(CCEAuditModel):
    image = models.FileField(upload_to='plank_images', blank=True, null=True)
    created = models.DateTimeField(verbose_name=None, auto_now_add=True)
    owner = models.ForeignKey(User)
    board = models.ForeignKey(Board)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    pinned = models.BooleanField(default=False)

    @staticmethod
    def is_owner(userobj, plank):
        return userobj == plank.owner

    @staticmethod
    def is_admin(userobj):
        return userobj.is_superuser or userobj.is_staff

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Plank, self).save(*args, **kwargs)

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

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from boards.models import Board


class Plank(models.Model):
    image = models.ImageField(upload_to='plank_images', blank=True, null=True)
    created = models.DateTimeField(verbose_name=None, auto_now_add=True)
    owner = models.ForeignKey(User)
    board = models.ForeignKey(Board)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    likes = models.IntegerField(default=0)
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

    @property
    def liked_users(self):
        return self.opinion_set.filter(liked=True).values_list('userprofile__pk', flat=True)

    @property
    def disliked_users(self):
        return self.opinion_set.filter(liked=False).values_list('userprofile__pk', flat=True)

    @property
    def total_likes(self):
        return self.likes
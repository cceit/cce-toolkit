from django.db import models
from django.utils.text import slugify


class Board(models.Model):
    image = models.ImageField(upload_to='board_images', blank=False, null=False)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return  self.name

    @staticmethod
    def is_admin(userobj):
        return userobj.is_superuser or userobj.is_staff

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Board, self).save(*args, **kwargs)
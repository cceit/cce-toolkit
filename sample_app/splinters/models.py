from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from planks.models import Plank


class Splint(models.Model):
    created = models.DateTimeField(verbose_name=None, auto_now_add=True)
    owner = models.ForeignKey(User)
    plank = models.ForeignKey(Plank)
    comment = models.TextField(max_length=1000, unique=False)
    slug = models.SlugField(unique=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.comment)
        self.comment = mark_safe(self.comment.replace("\n", "<br/>"))
        return super(Splint, self).save(*args, **kwargs)
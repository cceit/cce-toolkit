# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import cuser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plank',
            name='likes',
        ),
        migrations.AddField(
            model_name='plank',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plank',
            name='created_by',
            field=cuser.fields.CurrentUserField(related_name='planks_plank_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='plank',
            name='last_updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plank',
            name='last_updated_by',
            field=cuser.fields.CurrentUserField(related_name='planks_plank_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

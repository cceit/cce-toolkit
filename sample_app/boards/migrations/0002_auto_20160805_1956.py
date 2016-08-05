# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.conf import settings
import cuser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='created_by',
            field=cuser.fields.CurrentUserField(related_name='boards_board_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='last_updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='last_updated_by',
            field=cuser.fields.CurrentUserField(related_name='boards_board_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

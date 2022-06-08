# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django_currentuser.db.models import CurrentUserField
import toolkit.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('image', models.ImageField(upload_to=b'task_images')),
                ('attachment', models.FileField(null=True, upload_to=b'task_attachment', blank=True)),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(default=b'pending', max_length=128, blank=True, choices=[(b'pending', b'Pending'), (b'started', b'Started'), (b'complete', b'Complete')])),
                ('board', models.ForeignKey(related_name='tasks', on_delete=models.CASCADE, to='boards.Board')),
                ('created_by', CurrentUserField(related_name='tasks_task_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_updated_by', CurrentUserField(related_name='tasks_task_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(toolkit.models.mixins.ModelPermissionsMixin, models.Model),
        ),
    ]

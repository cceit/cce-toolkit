# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import toolkit.mixins.models
from django.conf import settings
import cuser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('summary', models.TextField(max_length=128)),
                ('description', models.TextField(max_length=256)),
                ('object_id', models.PositiveIntegerField()),
                ('absolute_url_name', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'ordering': ('-pk',),
                'db_table': 'activity_log',
            },
            bases=(toolkit.mixins.models.ModelPermissionsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(max_length=64)),
                ('logo', models.CharField(max_length=128, blank=True)),
                ('include_creator', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.Group')),
            ],
            options={
                'ordering': ('activity_type',),
                'db_table': 'activity_types',
            },
            bases=(toolkit.mixins.models.ModelPermissionsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='activity_type',
            field=models.ForeignKey(to='toolkit.ActivityType'),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='created_by',
            field=cuser.fields.CurrentUserField(related_name='toolkit_activitylog_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='last_updated_by',
            field=cuser.fields.CurrentUserField(related_name='toolkit_activitylog_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

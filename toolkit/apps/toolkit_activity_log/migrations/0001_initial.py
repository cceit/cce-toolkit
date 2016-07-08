# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import toolkit.models.mixins
import cuser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolkitActivityLog',
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
                'db_table': 'cce_toolkit_activity_log',
            },
            bases=(toolkit.models.mixins.ModelPermissionsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ToolkitActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(max_length=64)),
                ('logo', models.CharField(max_length=128, blank=True)),
                ('include_creator', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.Group')),
            ],
            options={
                'ordering': ('activity_type',),
                'db_table': 'cce_toolkit_activity_types',
            },
            bases=(toolkit.models.mixins.ModelPermissionsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='toolkitactivitylog',
            name='activity_type',
            field=models.ForeignKey(to='toolkit_activity_log.ToolkitActivityType'),
        ),
        migrations.AddField(
            model_name='toolkitactivitylog',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='toolkitactivitylog',
            name='created_by',
            field=cuser.fields.CurrentUserField(related_name='toolkit_activity_log_toolkitactivitylog_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='toolkitactivitylog',
            name='last_updated_by',
            field=cuser.fields.CurrentUserField(related_name='toolkit_activity_log_toolkitactivitylog_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

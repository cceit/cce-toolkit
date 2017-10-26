# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import cuser.fields
import toolkit.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64)),
                ('visibility', models.CharField(max_length=16, choices=[(b'private', b'Private'), (b'public', b'Public')])),
                ('query_string', models.TextField()),
                ('view', models.CharField(max_length=256)),
                ('created_by', cuser.fields.CurrentUserField(related_name='search_searchfilter_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_updated_by', cuser.fields.CurrentUserField(related_name='search_searchfilter_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'db_table': 'search_filters',
            },
            bases=(toolkit.models.mixins.ModelPermissionsMixin, models.Model),
        ),
    ]

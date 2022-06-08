# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django_currentuser.db.models import CurrentUserField
import toolkit.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('picture', models.FileField(null=True, upload_to=b'', blank=True)),
                ('created_by', CurrentUserField(related_name='profiles_profile_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_updated_by', CurrentUserField(related_name='profiles_profile_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(toolkit.models.mixins.ModelPermissionsMixin, models.Model),
        ),
    ]

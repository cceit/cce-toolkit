# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import cuser.fields
import toolkit.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('planks', '0002_auto_20160805_1956'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('splinters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Splinter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(max_length=1000)),
                ('slug', models.SlugField()),
                ('created_by', cuser.fields.CurrentUserField(related_name='splinters_splinter_last_created', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('last_updated_by', cuser.fields.CurrentUserField(related_name='splinters_splinter_last_updated', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('plank', models.ForeignKey(to='planks.Plank')),
            ],
            options={
                'abstract': False,
            },
            bases=(toolkit.models.mixins.ModelPermissionsMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='splint',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='splint',
            name='plank',
        ),
        migrations.DeleteModel(
            name='Splint',
        ),
    ]

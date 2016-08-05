# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('planks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Splint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(max_length=1000)),
                ('slug', models.SlugField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('plank', models.ForeignKey(to='planks.Plank')),
            ],
        ),
    ]

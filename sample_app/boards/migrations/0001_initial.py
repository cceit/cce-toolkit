# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'board_images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planks', '0002_auto_20160805_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plank',
            name='image',
            field=models.FileField(null=True, upload_to=b'plank_images', blank=True),
        ),
    ]

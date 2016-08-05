# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20160805_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='image',
            field=models.FileField(upload_to=b'board_images'),
        ),
    ]

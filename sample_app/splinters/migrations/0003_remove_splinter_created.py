# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splinters', '0002_auto_20160805_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='splinter',
            name='created',
        ),
    ]

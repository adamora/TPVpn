# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0004_auto_20160503_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.FloatField(null=True, blank=True),
        ),
    ]

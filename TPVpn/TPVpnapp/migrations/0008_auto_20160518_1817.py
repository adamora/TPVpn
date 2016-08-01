# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0007_auto_20160518_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_code',
            field=models.CharField(default=None, max_length=1000000, null=True, blank=True),
        ),
    ]

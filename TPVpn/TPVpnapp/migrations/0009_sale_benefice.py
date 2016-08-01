# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0008_auto_20160518_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='benefice',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
    ]

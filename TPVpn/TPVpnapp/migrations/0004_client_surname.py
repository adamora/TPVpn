# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0003_auto_20170110_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='surname',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0002_provider_market'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='market',
            field=models.ForeignKey(default=None, to='TPVpnapp.Market'),
        ),
    ]

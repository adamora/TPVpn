# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='market',
            field=models.ForeignKey(blank=True, to='TPVpnapp.Market', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0004_client_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='max_negative_wallet',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='stock_enabled',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='worker',
        ),
        migrations.AddField(
            model_name='configuration',
            name='invoice_header',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='market',
            field=models.OneToOneField(default=1, to='TPVpnapp.Market'),
            preserve_default=False,
        ),
    ]

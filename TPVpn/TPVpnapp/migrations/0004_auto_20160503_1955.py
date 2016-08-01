# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0003_auto_20160429_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='reciverCli',
            field=models.ForeignKey(default=None, blank=True, to='TPVpnapp.Client', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='reciver',
            field=models.ForeignKey(related_name='reciver', default=None, blank=True, to='TPVpnapp.Worker', null=True),
        ),
    ]

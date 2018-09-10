# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0005_auto_20170114_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='TPVpnapp.Offer', null=True),
        ),
    ]

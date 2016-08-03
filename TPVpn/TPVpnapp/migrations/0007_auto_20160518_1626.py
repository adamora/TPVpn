# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0006_auto_20160518_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsale',
            name='product',
            field=models.ForeignKey(default=None, blank=True, to='TPVpnapp.Product', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='segSocial',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterUniqueTogether(
            name='worker',
            unique_together=set([('market', 'segSocial'), ('market', 'dni')]),
        ),
    ]

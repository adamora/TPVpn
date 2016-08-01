# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0005_product_offer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(default=1.0, max_length=10)),
                ('sellPrice', models.FloatField(null=True, blank=True)),
                ('totAmount', models.FloatField(null=True, blank=True)),
                ('product', models.ForeignKey(default=None, to='TPVpnapp.Product')),
            ],
        ),
        migrations.RemoveField(
            model_name='productbill',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productbill',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='subtotal',
        ),
        migrations.DeleteModel(
            name='ProductBill',
        ),
        migrations.AddField(
            model_name='productsale',
            name='sale',
            field=models.ForeignKey(default=None, to='TPVpnapp.Sale'),
        ),
    ]

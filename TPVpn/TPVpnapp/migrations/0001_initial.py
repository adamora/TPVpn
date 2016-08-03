# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('name', models.CharField(max_length=120)),
                ('image', models.ImageField(default=b'clients/default/img.jpg', null=True, upload_to=b'clients/profile', blank=True)),
                ('dni', models.CharField(max_length=9, unique=True, serialize=False, primary_key=True)),
                ('email', models.EmailField(default=None, max_length=254, null=True, blank=True)),
                ('tel', models.IntegerField(default=None, null=True, blank=True)),
                ('wallet', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='FullDirection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('postalCode', models.CharField(max_length=5)),
                ('direction', models.CharField(max_length=100)),
                ('numDir', models.CharField(default=b'S/N', max_length=4)),
                ('stairs', models.CharField(default=b'', max_length=20, null=True, blank=True)),
                ('numFlat', models.IntegerField(null=True, blank=True)),
                ('door', models.CharField(default=b'', max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('kindActivity', models.CharField(max_length=250, null=True, blank=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('secretKey', models.CharField(max_length=16)),
                ('secretKey2', models.CharField(max_length=16)),
                ('tel', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('direction', models.ForeignKey(blank=True, to='TPVpnapp.FullDirection', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=500)),
                ('typeNote', models.CharField(max_length=20, choices=[(b'normal', b'normal'), (b'alert', b'alert'), (b'warning', b'warning')])),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('category', models.CharField(default=b'Ninguna', max_length=120)),
                ('subcategory', models.CharField(default=b'Ninguna', max_length=120)),
                ('brand', models.CharField(default=b'Blanca', max_length=120)),
                ('buyPrice', models.FloatField(max_length=10, null=True, blank=True)),
                ('sellPrice', models.FloatField(max_length=10)),
                ('amount', models.FloatField(max_length=10, null=True, blank=True)),
                ('kind', models.CharField(default=b'Unidades', max_length=20, choices=[(b'Unidades', b'Unidades'), (b'Kilos', b'Kilos'), (b'Gramos', b'Gramos')])),
                ('iva', models.IntegerField(default=21, choices=[(21, b'21%'), (10, b'10%'), (4, b'4%')])),
                ('barCode', models.CharField(default=b'Vacio', max_length=120, null=True, blank=True)),
                ('image', models.ImageField(default=b'products/default/product.png', null=True, upload_to=b'products/uploaded', blank=True)),
                ('market', models.ForeignKey(related_name='market', to='TPVpnapp.Market')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(default=1.0, max_length=10)),
                ('sellPrice', models.FloatField(max_length=10)),
                ('totAmount', models.FloatField(default=0.0, max_length=100)),
                ('product', models.ForeignKey(default=None, to='TPVpnapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('namePro', models.CharField(max_length=100)),
                ('tel', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sale_code', models.CharField(default=None, max_length=1000000)),
                ('subtotal', models.FloatField(default=0.0, max_length=100)),
                ('totAmount', models.FloatField(default=0.0, max_length=100, blank=True)),
                ('usedWallet', models.FloatField(default=0.0, max_length=100, blank=True)),
                ('recivedAmount', models.FloatField(default=0.0, max_length=100, blank=True)),
                ('devolution', models.FloatField(default=0.0, max_length=100, blank=True)),
                ('done', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(default=None, blank=True, to='TPVpnapp.Client', null=True)),
                ('market', models.ForeignKey(to='TPVpnapp.Market')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('dni', models.CharField(max_length=9, unique=True, serialize=False, primary_key=True)),
                ('genre', models.CharField(max_length=20, choices=[(b'Hombre', b'Hombre'), (b'Mujer', b'Mujer')])),
                ('segSocial', models.CharField(unique=True, max_length=12)),
                ('tel1', models.IntegerField()),
                ('tel2', models.IntegerField(null=True, blank=True)),
                ('image', models.ImageField(default=b'users/default/img.jpg', upload_to=b'users/profile')),
                ('home', models.ForeignKey(blank=True, to='TPVpnapp.FullDirection', null=True)),
                ('market', models.ForeignKey(blank=True, to='TPVpnapp.Market', null=True)),
                ('user', models.OneToOneField(default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='seller',
            field=models.ForeignKey(to='TPVpnapp.Worker'),
        ),
        migrations.AddField(
            model_name='productbill',
            name='sale',
            field=models.ForeignKey(default=None, to='TPVpnapp.Sale'),
        ),
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(to='TPVpnapp.Provider'),
        ),
        migrations.AddField(
            model_name='notification',
            name='reciver',
            field=models.ForeignKey(related_name='reciver', default=None, to='TPVpnapp.Worker'),
        ),
        migrations.AddField(
            model_name='notification',
            name='writer',
            field=models.ForeignKey(related_name='writer', default=None, blank=True, to='TPVpnapp.Worker', null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='market',
            field=models.ForeignKey(to='TPVpnapp.Market'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TPVpnapp', '0002_auto_20170108_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_method', models.CharField(max_length=120, null=True, blank=True)),
                ('owner_name', models.CharField(max_length=120, null=True, blank=True)),
                ('owner_surname', models.CharField(max_length=120, null=True, blank=True)),
                ('owner_nif', models.CharField(max_length=120, null=True, blank=True)),
                ('bank_name', models.CharField(max_length=120, null=True, blank=True)),
                ('account_number', models.CharField(max_length=120, null=True, blank=True)),
                ('subscription', models.FloatField(null=True, blank=True)),
                ('frequency', models.CharField(max_length=120, null=True, blank=True)),
                ('observations', models.CharField(max_length=500, null=True, blank=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 1, 10, 18, 53, 51, 312101, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='expire_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='home',
            field=models.ForeignKey(blank=True, to='TPVpnapp.FullDirection', null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='tel2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='bank',
            field=models.ForeignKey(blank=True, to='TPVpnapp.BankData', null=True),
        ),
    ]

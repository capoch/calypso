# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0046_auto_20161111_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomitem',
            name='days_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='guest',
            name='discount',
            field=models.FloatField(default=0, verbose_name='Discount in %'),
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
    ]
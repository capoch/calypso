# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-26 01:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0071_auto_20161126_0902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='gender',
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
    ]

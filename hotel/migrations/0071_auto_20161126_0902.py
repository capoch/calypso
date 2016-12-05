# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-26 01:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0070_auto_20161126_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 11, 26, 1, 2, 36, 349461, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
    ]

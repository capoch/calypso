# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 05:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0033_auto_20161110_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='checkin_date',
            field=models.DateField(default=datetime.datetime(2016, 11, 10, 5, 24, 23, 122928, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 11, 10, 5, 24, 23, 125804, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
    ]

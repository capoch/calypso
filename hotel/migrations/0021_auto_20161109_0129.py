# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 17:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0020_auto_20161109_0126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='motorcycle',
            old_name='notels',
            new_name='notes',
        ),
        migrations.AlterField(
            model_name='guest',
            name='checkin_date',
            field=models.DateField(default=datetime.datetime(2016, 11, 8, 17, 28, 57, 769162, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 11, 8, 17, 28, 57, 772227, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
    ]
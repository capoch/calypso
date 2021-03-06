# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 02:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0061_auto_20161124_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitem',
            name='warning',
            field=models.BooleanField(default=False),
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

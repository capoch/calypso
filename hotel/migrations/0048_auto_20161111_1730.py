# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0047_auto_20161111_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
    ]

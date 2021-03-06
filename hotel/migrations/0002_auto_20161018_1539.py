# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='guest',
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hotel.RoomType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Guest',
        ),
    ]

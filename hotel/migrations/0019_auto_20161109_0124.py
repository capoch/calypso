# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 17:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0018_auto_20161109_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motorcycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=30)),
                ('clutch', models.CharField(choices=[('M', 'Manual'), ('A', 'Automatic')], max_length=1)),
                ('registration', models.CharField(max_length=100)),
                ('notels', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='guest',
            name='checkin_date',
            field=models.DateField(default=datetime.datetime(2016, 11, 8, 17, 24, 12, 551246, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 11, 8, 17, 24, 12, 554294, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.Item'),
        ),
        migrations.AddField(
            model_name='guest',
            name='motorcycle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Guest', to='hotel.Motorcycle'),
        ),
    ]

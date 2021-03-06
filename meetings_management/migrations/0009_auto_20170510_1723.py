# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-10 20:23
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('meetings_management', '0008_auto_20170510_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingroomrequest',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='amount of people'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetingroomrequest',
            name='supplies',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, default=[], size=None, verbose_name='supplies to use'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meetingroom',
            name='available_from',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 10, 6, 0, 0, 645211, tzinfo=utc), verbose_name='available from'),
        ),
        migrations.AlterField(
            model_name='meetingroom',
            name='available_until',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 10, 21, 0, 0, 645331, tzinfo=utc), verbose_name='available until'),
        ),
    ]

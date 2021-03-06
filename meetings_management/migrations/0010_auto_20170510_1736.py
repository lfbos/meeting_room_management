# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-10 20:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('meetings_management', '0009_auto_20170510_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingroom',
            name='available_from',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 10, 6, 0, 0, 33903, tzinfo=utc), verbose_name='available from'),
        ),
        migrations.AlterField(
            model_name='meetingroom',
            name='available_until',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 10, 21, 0, 0, 33966, tzinfo=utc), verbose_name='available until'),
        ),
        migrations.AlterField(
            model_name='meetingroomrequest',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user_requests', to='meetings_management.MeetingRoomUser'),
        ),
    ]

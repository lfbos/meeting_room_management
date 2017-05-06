# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-05 21:42
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('meetings_management', '0002_auto_20170505_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingRoomReservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, verbose_name='metadata')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date and time of creation')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='date and time of last update')),
                ('reserved_from', models.DateTimeField(verbose_name='reserved from')),
                ('reserved_until', models.DateTimeField(verbose_name='reserved until')),
                ('amount', models.IntegerField(verbose_name='amount of people')),
                ('supplies', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, size=None, verbose_name='supplies to use')),
            ],
            options={
                'verbose_name': 'meeting room reservation',
                'verbose_name_plural': 'meeting room reservations',
            },
        ),
        migrations.AlterField(
            model_name='meetingroom',
            name='available_from',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 5, 6, 0, 0, 629370, tzinfo=utc), verbose_name='available from'),
        ),
        migrations.AlterField(
            model_name='meetingroom',
            name='available_until',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 5, 21, 0, 0, 629468, tzinfo=utc), verbose_name='available until'),
        ),
        migrations.AddField(
            model_name='meetingroomreservation',
            name='meeting_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='meetings_management.MeetingRoom'),
        ),
        migrations.AddField(
            model_name='meetingroomreservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='meetings_management.MeetingRoomUser'),
        ),
    ]

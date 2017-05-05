# coding=utf-8
from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.mixins import BaseMixin


class MeetingRoom(BaseMixin):
    name = models.CharField(max_length=64, verbose_name=_('name'))
    location = models.CharField(max_length=64, verbose_name=_('location'))
    capacity = models.IntegerField(verbose_name=_('capacity'))
    available_from = models.DateTimeField(
        default=timezone.now().replace(hour=6, minute=0, second=0),
        verbose_name=_('available from')
    )
    available_until = models.DateTimeField(
        default=timezone.now().replace(hour=21, minute=0, second=0),
        verbose_name=_('available until')
    )
    supplies = ArrayField(
        models.CharField(max_length=64),
        default=['Proyector', 'Pizarrón'],
        help_text=_('Add supplies separated by comma'),
        verbose_name=_('supplies')
    )

    def __str__(self):
        return "{} - {}".format(self.name, self.location)

    class Meta:
        verbose_name = _('meeting room')
        verbose_name_plural = _('meeting rooms')

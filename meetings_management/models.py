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

    def __unicode__(self):
        return "{} - {}".format(self.name, self.location)

    class Meta:
        verbose_name = _('meeting room')
        verbose_name_plural = _('meeting rooms')


class MeetingRoomUser(BaseMixin):
    ROLE_EMPLOYEE = 0
    ROLE_ADMIN = 1
    ROLES = (
        (ROLE_EMPLOYEE, _('Employee')),
        (ROLE_ADMIN, _('Administrator'))
    )

    user = models.OneToOneField(
        'auth.User',
        related_name='meeting_room_user'
    )

    role = models.PositiveSmallIntegerField(
        default=ROLE_EMPLOYEE,
        choices=ROLES,
        verbose_name=_('Role')
    )

    def __unicode__(self):
        return "{} - {}".format(
            {
                0: _("Employee"),
                1: _("Administrator")
            }[self.role],
            self.user.get_full_name() or self.user.username
        )

    class Meta:
        verbose_name = _('meeting room user')
        verbose_name_plural = _('meeting room users')


class MeetingRoomReservation(BaseMixin):
    meeting_room = models.ForeignKey(
        'MeetingRoom',
        related_name='reservations'
    )

    user = models.ForeignKey(
        'MeetingRoomUser',
        related_name='reservations'
    )

    reserved_from = models.DateTimeField(verbose_name=_('reserved from'))
    reserved_until = models.DateTimeField(verbose_name=_('reserved until'))
    amount = models.IntegerField(verbose_name=_('amount of people'))
    supplies = ArrayField(
        models.CharField(max_length=64),
        blank=True,
        verbose_name=_('supplies to use')
    )

    confirmed = models.BooleanField(
        default=False,
        verbose_name=_('reservation confirmed')
    )

    def __unicode__(self):
        return "{} - {}".format(
            self.meeting_room.name,
            self.user.user.get_full_name() or self.user.user.username
        )

    class Meta:
        verbose_name = _('meeting room reservation')
        verbose_name_plural = _('meeting room reservations')


class MeetingRoomRequest(BaseMixin):
    user = models.ForeignKey(
        'MeetingRoomUser',
        related_name='requests'
    )

    to_user = models.ForeignKey(
        'MeetingRoomUser',
        related_name='to_user_requests'
    )

    reservation = models.ForeignKey(
        'MeetingRoomReservation'
    )

    message = models.CharField(
        max_length=128,
        verbose_name=_('user message')
    )

    reserved_from = models.DateTimeField(
        verbose_name=_('need to reserve from')
    )

    reserved_until = models.DateTimeField(
        verbose_name=_('need to reserve until')
    )

    amount = models.IntegerField(verbose_name=_('amount of people'))

    supplies = ArrayField(
        models.CharField(max_length=64),
        blank=True,
        verbose_name=_('supplies to use')
    )

    def __unicode__(self):
        return "{}, {}".format(
            self.to_user.user.get_full_name() or self.to_user.user.username,
            self.created.strftime('%d/%m/%y %H:%M:%S')
        )

    class Meta:
        verbose_name = _('user request')
        verbose_name_plural = _('user requests')
        unique_together = (('to_user', 'reservation'),)

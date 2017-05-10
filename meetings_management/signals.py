from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from meetings_management.exceptions import (
    ReservationCollisionException,
    ReservationReservedCollisionException
)
from meetings_management.models import MeetingRoomReservation


@receiver(post_save, sender=MeetingRoomReservation)
def check_meeting_room_availability(sender, instance, created, raw, **kwargs):
    if created and not raw:
        q1 = Q(reserved_from__range=(instance.reserved_from, instance.reserved_until))
        q2 = Q(reserved_until__range=(instance.reserved_from, instance.reserved_until))

        reservations = MeetingRoomReservation.objects.filter(q1 | q2) \
            .filter(meeting_room=instance.meeting_room) \
            .exclude(pk=instance.pk)

        reserved = reservations.filter(confirmed=False)
        confirmed = reservations.filter(confirmed=True)

        if confirmed.count() > 0:
            MeetingRoomReservation.objects.filter(pk=instance.pk).delete()
            raise ReservationCollisionException('Error! Reservations already confirmed at that time')
        elif reserved.count() > 0:
            MeetingRoomReservation.objects.filter(pk=instance.pk).delete()
            raise ReservationReservedCollisionException(
                'Reservations exist at that time, contact with the owner if '
                'you need urgent the room'
            )

from django.db.models.signals import pre_save
from django.dispatch import receiver

from meetings_management.exceptions import ReservationCollisionException
from meetings_management.models import MeetingRoomReservation


@receiver(pre_save, sender=MeetingRoomReservation)
def check_meeting_room_availability(sender, instance, raw, **kwargs):
    if not MeetingRoomReservation.objects.filter(
            reserved_from__gte=instance.reserved_from,
            reserved_until__lte=instance.reserved_until):
        raise ReservationCollisionException('Error! Reservations already exist at that time')

from django.contrib import admin

from core.admin import BaseModelAdmin
from meetings_management.models import (
    MeetingRoom,
    MeetingRoomUser,
    MeetingRoomReservation,
    MeetingRoomRequest
)

admin.site.register(MeetingRoom, BaseModelAdmin)
admin.site.register(MeetingRoomUser, BaseModelAdmin)
admin.site.register(MeetingRoomReservation, BaseModelAdmin)
admin.site.register(MeetingRoomRequest, BaseModelAdmin)

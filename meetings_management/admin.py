from django.contrib import admin

from core.admin import BaseModelAdmin
from meetings_management.models import MeetingRoom, MeetingRoomUser

admin.site.register(MeetingRoom, BaseModelAdmin)
admin.site.register(MeetingRoomUser, BaseModelAdmin)

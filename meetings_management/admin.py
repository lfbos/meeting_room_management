from django.contrib import admin

from core.admin import BaseModelAdmin
from meetings_management.models import MeetingRoom

admin.site.register(MeetingRoom, BaseModelAdmin)

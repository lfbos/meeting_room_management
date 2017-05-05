from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MeetingsManagementConfig(AppConfig):
    name = 'meetings_management'
    label = 'meetings_management'
    verbose_name = _('Meetings Management')

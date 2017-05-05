import uuid

from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _


class BaseMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    metadata = JSONField(
        blank=True,
        default=dict(),
        verbose_name=_('metadata')
    )

    created = models.DateTimeField(auto_now_add=True,
                                   editable=False,
                                   verbose_name=_('date and time of creation'))
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('date and time of last update')
    )

    class Meta:
        abstract = True

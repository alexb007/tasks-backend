from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseTimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Last updated at"))

    class Meta:
        abstract = True

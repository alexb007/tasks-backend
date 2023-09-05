from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseTimestampModel


class TaskAttachment(BaseTimestampModel):
    task = models.ForeignKey(
        "task.Task",
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to="attachments/")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("User")
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Task attachment")
        verbose_name_plural = _("Task attachments")

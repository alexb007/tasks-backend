from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseTimestampModel


class TaskComment(BaseTimestampModel):
    task = models.ForeignKey(
        'task.Task',
        on_delete=models.CASCADE,
    )
    comment = models.TextField(
        max_length=1000,
        verbose_name=_('Comment text')
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Task comment')
        verbose_name_plural = _('Task comments')

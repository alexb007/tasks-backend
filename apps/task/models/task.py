from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, ConcurrentTransitionMixin, transition

from apps.core.models import BaseTimestampModel


class Task(ConcurrentTransitionMixin, BaseTimestampModel):
    class State:
        TODO = "todo"
        DONE = "done"

    STATE_CHOICES = (
        (State.TODO, _("To do")),
        (State.DONE, _("Done")),
    )

    name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Task Name")
    )
    description = models.TextField(max_length=3000, verbose_name=_("Task Description"))
    deadline = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Task Deadline")
    )
    creator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("Created by")
    )
    assigned = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        verbose_name=_("Assigned to"),
    )
    state = FSMField(default=State.TODO, choices=STATE_CHOICES)

    @transition(field=state, source="*", target=State.DONE)
    def mark_done(self):
        pass

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

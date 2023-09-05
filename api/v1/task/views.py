from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.v1.task.serializers import TaskSerializer
from apps.task.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()

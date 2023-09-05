from rest_framework import viewsets


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
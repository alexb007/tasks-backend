from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.v1.task.serializers import TaskSerializer, TaskAssignSerializer, TaskCommentSerializer, \
    TaskCommentCreateSerializer
from apps.task.models import Task, TaskComment


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Task.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('creator', 'assigned', 'state')
    search_fields = ('name', )

    def get_serializer_class(self):
        if action == 'assign':
            return TaskAssignSerializer
        return self.serializer_class

    @swagger_auto_schema(
        operation_description='POST /tasks/{id}/complete/',
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties=None), responses={
            status.HTTP_200_OK: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description='Success Response',
                examples={
                    "application/json": {
                        "success": True,
                        "message": "task <TaskName> with id <task_id> marked as done"
                    }
                }
            )
        })
    @action(detail=True, methods=['patch'])
    def complete(self, request, *args, **kwargs):
        task = self.get_object()
        task.mark_done()
        task.save()
        return Response({
            'success': True,
            'message': f'task {task.name} with id {task.id} marked as done'
        })

    @swagger_auto_schema(
        operation_description='POST /tasks/{id}/assign/',
        responses={
            status.HTTP_200_OK: openapi.Response(
                type=openapi.TYPE_OBJECT,
                schema=TaskSerializer,
                description='Success Response',
            ),
        })
    @action(detail=True, methods=['patch'], serializer_class=TaskAssignSerializer)
    def assign(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            task.assigned = serializer.validated_data['user']
            task.save()
            return Response(TaskSerializer(task).data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='POST /tasks/{id}/comment/',
        responses={
            status.HTTP_200_OK: openapi.Response(
                type=openapi.TYPE_OBJECT,
                schema=TaskCommentSerializer,
                description='Success Response',
            ),
        })
    @action(detail=True, methods=['post'], serializer_class=TaskCommentCreateSerializer)
    def comment(self, request, *args, **kwargs):
        task = self.get_object()
        try:
            task_comment = TaskComment.objects.create(
                task=task,
                comment=request.data.get('comment'),
                user=request.user,
            )
            return Response(TaskCommentSerializer(task_comment).data)
        except Exception as ex:
            print(ex)
            return Response(
                ex,
                status=status.HTTP_400_BAD_REQUEST
            )


class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    queryset = TaskComment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('task', 'user',)
    search_fields = ('comment', )


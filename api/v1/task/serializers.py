from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from apps.task.models import Task, TaskComment, TaskAttachment

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def to_representation(self, instance):
        data = super(TaskSerializer, self).to_representation(instance)
        data["creator"] = UserSerializer(instance.creator).data
        if instance.assigned is not None:
            data["assigned"] = UserSerializer(instance.assigned).data
        return data

    class Meta:
        model = Task
        fields = "__all__"


class TaskAssignSerializer(serializers.Serializer):
    # Serializer for assigning user to the task
    user = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all()
    )


class TaskCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def to_representation(self, instance):
        data = super(TaskCommentSerializer, self).to_representation(instance)
        data["user"] = UserSerializer(instance.user).data
        return data

    class Meta:
        model = TaskComment
        fields = "__all__"


class TaskCommentCreateSerializer(TaskCommentSerializer):
    task = serializers.PrimaryKeyRelatedField(read_only=True)


class TaskAttachmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def to_representation(self, instance):
        data = super(TaskAttachmentSerializer, self).to_representation(instance)
        data["user"] = UserSerializer(instance.creator).data
        return data

    class Meta:
        model = TaskAttachment
        fields = "__all__"

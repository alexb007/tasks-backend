from rest_framework import routers

from api.v1.task.views import TaskViewSet, TaskCommentViewSet, TaskAttachmentViewSet

router = routers.SimpleRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"tasks/comments", TaskCommentViewSet)
router.register(r"tasks/attachments", TaskAttachmentViewSet)

urlpatterns = []

urlpatterns += router.urls

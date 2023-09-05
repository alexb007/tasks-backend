from django.urls import path, include
from rest_framework import routers

from api.v1.task.views import TaskViewSet

router = routers.SimpleRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = []

urlpatterns += router.urls

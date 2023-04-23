from django.urls import path, include
from rest_framework import routers

from sm_app.views import PostViewSet

router = routers.DefaultRouter()
router.register("", PostViewSet, basename="post-list")

urlpatterns = [path("", include(router.urls))]

app_name = "sm_app"

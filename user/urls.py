from django.urls import path, include
from rest_framework import routers

from user.views import UserViewSet

router = routers.DefaultRouter()
router.register("user", UserViewSet, basename="user-list")

urlpatterns = [path("", include(router.urls))]

app_name = "user"
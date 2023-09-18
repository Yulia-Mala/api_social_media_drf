from django.urls import path, include
from rest_framework import routers

from sm_app.views import PostViewSet, like_post, unlike_post

router = routers.DefaultRouter()
router.register("", PostViewSet, basename="post-list")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/like/", like_post, name="like_post"),
    path("<int:pk>/unlike/", unlike_post, name="unlike_post"),
]

app_name = "sm_app"

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import (
    CreateUserView,
    UpdateUserView,
    UserListView,
    UserRetrieveView,
    follow_user,
    unfollow_user,
    UserFollowers,
    UserInfluencers,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("my-profile/", UpdateUserView.as_view(), name="manage"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/<int:pk>/", UserRetrieveView.as_view(), name="user-detail"),
    path("users/<int:pk>/follow/", follow_user, name="follow_user"),
    path("users/<int:pk>/unfollow/", unfollow_user, name="unfollow_user"),
    path("my-profile/followers/", UserFollowers.as_view(), name="followers"),
    path("my-profile/influencers/", UserInfluencers.as_view(), name="influencers"),
]

app_name = "user"

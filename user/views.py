from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics

from user.models import UserFollowing
from user.serializers import UserListSerializer, UserDetailSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.exclude(id=self.request.user.id)
        username = self.request.query_params.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


class UserFollowers(UserListView):
    def get_queryset(self):
        current_user = self.request.user
        followers = UserFollowing.objects.filter(
            user_who_influence=current_user
        ).values_list("user_who_follow__id")
        return get_user_model().objects.filter(id__in=followers)


class UserInfluencers(UserListView):
    def get_queryset(self):
        current_user = self.request.user
        influencers = UserFollowing.objects.filter(
            user_who_follow=current_user
        ).values_list("user_who_influence__id")
        return get_user_model().objects.filter(id__in=influencers)


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        return get_user_model().objects.all()


@api_view(["GET"])
def follow_user(request, pk=None):
    current_user = request.user
    try:
        user_to_follow = get_user_model().objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(
            data="Check that such a user exists.",
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        UserFollowing.objects.create(
            user_who_follow=current_user, user_who_influence=user_to_follow
        )
        return Response(status=status.HTTP_201_CREATED)

    except ValidationError:
        return Response(
            data="User cannot follow oneself. "
            "Check that you don't try to follow user who you have already follow",
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def unfollow_user(request, pk=None):
    current_user = request.user
    try:
        user_to_unfollow = get_user_model().objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(
            data="Check that such a user exists.",
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        relation = UserFollowing.objects.get(
            user_who_follow=current_user, user_who_influence=user_to_unfollow
        )
    except ObjectDoesNotExist:
        return Response(
            data="You don't follow such a user",
            status=status.HTTP_400_BAD_REQUEST,
        )
    relation.delete()
    return Response(status=status.HTTP_200_OK)

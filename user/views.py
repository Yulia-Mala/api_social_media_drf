from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User, UserFollowing
from user.serializers import UserListSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserListSerializer

    @action(methods=["GET"], detail=True, url_path="follow_user")
    def follow_user(self, request, pk=None):
        current_user = self.request.user
        try:
            user_to_follow = User.objects.get(pk=pk)
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

    @action(methods=["GET"], detail=True, url_path="unfollow_user")
    def unfollow_user(self, request, pk=None):
        current_user = self.request.user
        try:
            user_to_unfollow = User.objects.get(pk=pk)
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

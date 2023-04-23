from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from sm_app.models import Post, Like
from sm_app.serializers import PostSerializer
from user.models import UserFollowing


class PostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        my_posts = self.request.query_params.get("my_posts")
        text = self.request.query_params.get("text")
        current_user = self.request.user

        if my_posts == "yes":
            return Post.objects.filter(user=current_user)

        if text:
            return Post.objects.filter(text__icontains=text)

        influencers = UserFollowing.objects.filter(
            user_who_follow=current_user
        ).values_list("user_who_influence")
        return Post.objects.filter(user__in=influencers)

    def get_serializer_class(self):
        if self.action == "list":
            return PostSerializer
        if self.action == "create":
            return PostSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action in ("destroy", "partial_update", "update"):
            raise MethodNotAllowed(self.action)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
def like_post(request, pk=None):
    current_user = request.user
    try:
        post_to_like = Post.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(
            data="Check that such a post exists.",
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        Like.objects.create(user=current_user, post=post_to_like)
        return Response(status=status.HTTP_201_CREATED)

    except ValidationError:
        return Response(
            data="Check that you don't try to like 1 post more than 1 time",
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def unlike_post(request, pk=None):
    current_user = request.user
    try:
        post_to_unlike = Post.objects.get(pk=pk)
        like = Like.objects.filter(user=current_user, post=post_to_unlike)
    except ObjectDoesNotExist:
        return Response(
            data="Check that such a post exists and you have already like it",
            status=status.HTTP_400_BAD_REQUEST,
        )
    like.delete()
    return Response(status=status.HTTP_200_OK)

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from sm_app.models import Post, Like
from sm_app.serializers import PostSerializer
from user.models import UserFollowing


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ["get", "post", "head"]

    def get_queryset(self):
        my_posts = self.request.query_params.get("my_posts")
        text = self.request.query_params.get("text")
        influencers = self.request.query_params.get("influencers")

        queryset = Post.objects.all().prefetch_related("likes")
        current_user = self.request.user

        if my_posts == "yes":
            queryset = queryset.filter(user=current_user)

        if text:
            queryset = queryset.filter(text__icontains=text)

        if influencers == "yes":
            influencers_list = UserFollowing.objects.filter(
                user_who_follow=current_user
            ).values_list("user_who_influence")
            queryset = queryset.filter(user__in=influencers_list)
        return queryset

    def get_permissions(self):
        if self.action in ("update", "delete", "partial_update"):
            raise MethodNotAllowed(method=self.request.method)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "my_posts",
                type=str,
                description="Retrieve only current user's posts"
                "Url format: ?my_posts=yes",
                required=False,
            ),
            OpenApiParameter(
                "influencers",
                type=str,
                description="Retrieve only user's influencer's posts"
                "Url format: ?influencers=yes",
                required=False,
            ),
            OpenApiParameter(
                "text",
                type=str,
                description="Retrieve posts which contain such a text. "
                "Case-insensitive Url format: url + ?text=abc",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@api_view(["GET"])
def like_post(request, pk=None):
    """Add authenticated user's like to the specific post"""
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
    """Remove authenticated user's like from the specific post"""
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

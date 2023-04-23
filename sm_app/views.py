from rest_framework import viewsets

from sm_app.models import Post
from sm_app.serializers import PostSerializer
from user.models import UserFollowing


class PostViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        current_user = self.request.user
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

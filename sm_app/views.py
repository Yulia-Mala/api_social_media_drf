from rest_framework import viewsets

from sm_app.models import Post
from sm_app.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

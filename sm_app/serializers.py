from rest_framework import serializers

from sm_app.models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "time", "user", "text", "image"]
        read_only_fields = ("user",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "post", "user", "time"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["post", "user"]

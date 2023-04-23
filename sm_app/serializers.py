from rest_framework import serializers

from sm_app.models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "time", "user", "text", "image"]
        read_only_fields = ("user",)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["text", "post", "user", "time"]
        read_only_fields = ("user",)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Like
        fields = ["post", "user"]
        read_only_fields = ("user",)

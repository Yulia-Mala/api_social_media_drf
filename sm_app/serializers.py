from rest_framework import serializers

from sm_app.models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["time", "user", "text", "image"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "post", "user", "time"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["post", "user"]

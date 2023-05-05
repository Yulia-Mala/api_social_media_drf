from rest_framework import serializers

from sm_app.models import Post, Like


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Like
        fields = ["user"]
        read_only_fields = ("user",)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "time", "user", "text", "image", "likes"]
        read_only_fields = [
            "user",
        ]

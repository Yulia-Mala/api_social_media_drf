from rest_framework import serializers

from user.models import User, UserFollowing


class UserWhoFollow(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["user_who_follow"]


class UserWhoInfluence(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ["user_who_influence"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "bio",
            "username",
            "birthday",
            "gender",
            "avatar",
            "influenced_by_counter",
            "followed_by_counter",
        )


class UserDetailSerializer(UserListSerializer):
    influenced_by = serializers.SerializerMethodField()
    followed_by = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserListSerializer.Meta.fields + (
            "influenced_by",
            "followed_by",
        )

    def get_influenced_by(self, user):
        influenced_by = []
        for ordered_dict in UserWhoInfluence(user.influenced_by.all(), many=True).data:
            user_id = ordered_dict["user_who_influence"]
            influenced_by.append(User.objects.get(id=user_id).username)
        return influenced_by

    def get_followed_by(self, user):
        followed_by = []
        for ordered_dict in UserWhoFollow(user.followed_by.all(), many=True).data:
            user_id = ordered_dict["user_who_follow"]
            followed_by.append(User.objects.get(id=user_id).username)
        return followed_by

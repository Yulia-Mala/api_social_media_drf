from django.contrib.auth import get_user_model
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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "bio",
            "username",
            "birthday",
            "gender",
            "avatar",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class UserListSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = UserSerializer.Meta.fields + (
            "influenced_by_counter",
            "followed_by_counter",
        )


class UserDetailSerializer(UserListSerializer):
    influenced_by = serializers.SerializerMethodField()
    followed_by = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = UserListSerializer.Meta.fields + (
            "influenced_by",
            "followed_by",
        )

    def get_influenced_by(self, user):
        influenced_by = []
        for ordered_dict in UserWhoInfluence(
            user.users_who_follow.all(), many=True
        ).data:
            user_id = ordered_dict["user_who_influence"]
            influenced_by.append(User.objects.get(id=user_id).username)
        return influenced_by

    def get_followed_by(self, user):
        followed_by = []
        for ordered_dict in UserWhoFollow(
            user.users_who_influence.all(), many=True
        ).data:
            user_id = ordered_dict["user_who_follow"]
            followed_by.append(User.objects.get(id=user_id).username)
        return followed_by

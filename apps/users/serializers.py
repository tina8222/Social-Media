from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import UserProfile, Follow, RestrictUser, BlockUser

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password" : {"write_only": True}
        }


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True,)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", required=False)

    class Meta:
        model = UserProfile
        fields = ["username", "bio", "avatar", "gender", "birth_date", "location"]


class FollowersListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="follower.username")
    first_name = serializers.CharField(source="follower.first_name")
    last_name = serializers.CharField(source="follower.last_name")


    class Meta:
        model = Follow
        fields = ["username", "first_name", "last_name", "created_at"]


class FollowingListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="following.username")
    first_name = serializers.CharField(source="following.first_name")
    last_name = serializers.CharField(source="following.last_name")

    class Meta:
        model = Follow
        fields = ["username", "first_name", "last_name", "created_at"]


class RestrictUserSerializer(serializers.ModelSerializer):
    restricted_user_username = serializers.CharField(source="restricted_user.username", read_only=True)
    restricted_user_email = serializers.EmailField(source="restricted_user.email", read_only=True)

    class Meta:
        model = RestrictUser
        fields = ["restricted_user_username", "restricted_user_email"]


class BlockUserSerializer(serializers.ModelSerializer):
    blocked_username = serializers.CharField(source="blocked.username",read_only=True)
    blocked_email = serializers.EmailField(source="blocked.email",read_only=True)

    class Meta:
        model = BlockUser
        fields = ("blocked_username","blocked_email","created_at")
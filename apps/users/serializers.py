from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import UserProfile, Follow

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value    

    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )


class LoginSerializer(serializers.Serializer):

    login = serializers.CharField(required=True)

    password = serializers.CharField(
        write_only=True,
        required=True,
    )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()



class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", required=False)

    class Meta:
        model = UserProfile
        fields = ["bio", "avatar", "gender", "birth_date", "location", "username"]


    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        if user_data:
            instance.user.username = user_data["username"]
            instance.user.save()

        return super().update(instance, validated_data)


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


class FollowersCountSerializer(serializers.Serializer):
    username = serializers.CharField()
    followers_count = serializers.IntegerField(default=0)

class  FollowingCountSerializer(serializers.Serializer):
    username = serializers.CharField()
    following_count = serializers.IntegerField(default=0)
